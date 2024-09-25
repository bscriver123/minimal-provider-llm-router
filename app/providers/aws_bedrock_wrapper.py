import json
from datetime import datetime, timezone
from typing import Any, AsyncGenerator, Optional
from uuid import uuid4

import boto3
from aiobotocore.session import AioSession, get_session
from fastapi import HTTPException, status
from loguru import logger

from .enums import ModelName

FOUNDATION_MODEL_NAME_TO_MODEL_ID: dict[ModelName, str] = {
    ModelName.claude_sonnet_3: "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0",  # noqa: E501
    ModelName.claude_sonnet_3_5: "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-20240620-v1:0",  # noqa: E501
}


class AWSBedrockWrapper:
    def __init__(self, region: str, model_name: ModelName, temperature: float, max_tokens: int):
        self.region = region
        self.model_name = model_name
        self.model_id = FOUNDATION_MODEL_NAME_TO_MODEL_ID.get(model_name)
        if self.model_id is None:
            raise ValueError(f"Model ID not found for model name {model_name}")
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.session: AioSession = get_session()

    @staticmethod
    def _translate_openai_to_bedrock(openai_messages: list[dict[str, str]]) -> list[dict[str, Any]]:
        bedrock_messages = []
        try:
            for message in openai_messages:
                role = message["role"]
                content = message["content"]

                bedrock_message = {"role": role, "content": [{"text": content}]}

                bedrock_messages.append(bedrock_message)

            return bedrock_messages
        except KeyError as e:
            logger.error("Missing key in OpenAI message: {}", e)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid message format",
            )

    @staticmethod
    def _translate_bedrock_response_to_openai(
        bedrock_response: dict[str, Any], model_name: str
    ) -> list[dict[str, str]]:
        try:
            created_timestamp = int(datetime.now().timestamp())

            response_id = bedrock_response["ResponseMetadata"]["RequestId"]
            role = bedrock_response["output"]["message"]["role"]
            output_message = bedrock_response["output"]["message"]["content"][0]["text"]

            stop_reason_map = {
                "end_turn": "stop",
            }
            stop_reason = stop_reason_map.get(bedrock_response["stopReason"], "stop")

            input_tokens = bedrock_response["usage"]["inputTokens"]
            output_tokens = bedrock_response["usage"]["outputTokens"]
            total_tokens = bedrock_response["usage"]["totalTokens"]

            openai_response = {
                "choices": [
                    {
                        "finish_reason": stop_reason,
                        "index": 0,
                        "message": {"content": output_message, "role": role},
                        "logprobs": None,
                    }
                ],
                "created": created_timestamp,
                "id": response_id,
                "model": model_name,
                "object": "chat.completion",
                "usage": {
                    "completion_tokens": output_tokens,
                    "prompt_tokens": input_tokens,
                    "total_tokens": total_tokens,
                },
            }
            return openai_response
        except KeyError as e:
            logger.error("Missing key in Bedrock response: {}", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to process completion",
            )

    async def create_completion(self, messages: list[dict[str, str]]) -> dict:
        formatted_messages = self._translate_openai_to_bedrock(messages)
        async with self.session.create_client("bedrock-runtime", region_name=self.region) as client:
            try:
                response = await client.converse(
                    modelId=self.model_id,
                    messages=formatted_messages,
                    inferenceConfig={
                        "maxTokens": self.max_tokens,
                        "temperature": self.temperature,
                    },
                )
                return self._translate_bedrock_response_to_openai(response, self.model_name.value)
            except boto3.exceptions.Boto3Error as e:
                logger.error("Boto3 error during completion: {}", e)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to process completion",
                )

    @staticmethod
    def _format_chunk(
        chunk: dict[str, Any],
        model_name: str,
        message_id: str,
        created_time: int,
        system_fingerprint: str,
    ) -> Optional[dict[str, Any]]:
        delta_content = None
        role = None
        finish_reason = None
        try:
            if "contentBlockStop" in chunk:
                return None
            elif "messageStart" in chunk:
                delta_content = ""
                role = chunk["messageStart"]["role"]
            elif "contentBlockDelta" in chunk:
                delta_content = chunk["contentBlockDelta"]["delta"]["text"]
            elif "messageStop" in chunk:
                finish_reason = "stop"
            if delta_content is not None or finish_reason == "stop":
                return {
                    "id": message_id,
                    "choices": [
                        {
                            "delta": {
                                "content": delta_content,
                                "function_call": None,
                                "role": role,
                                "tool_calls": None,
                            },
                            "finish_reason": finish_reason,
                            "index": 0,
                            "logprobs": None,
                        }
                    ],
                    "created": created_time,
                    "model": model_name,
                    "object": "chat.completion.chunk",
                    "system_fingerprint": system_fingerprint,
                    "usage": None,
                }
        except KeyError as e:
            logger.error("Missing key in Bedrock stream chunk: {}", e)
        return None

    async def get_stream_content(self, messages: list[dict[str, str]]) -> AsyncGenerator[str, None]:
        formatted_messages = self._translate_openai_to_bedrock(messages)
        session = get_session()
        try:
            async with session.create_client("bedrock-runtime", region_name=self.region) as client:
                response = await client.converse_stream(
                    modelId=self.model_id,
                    messages=formatted_messages,
                    inferenceConfig={"temperature": self.temperature, "maxTokens": self.max_tokens},
                )
                message_id = f"chatcmpl-{uuid4()}"
                created_time = int(datetime.now(timezone.utc).timestamp())
                system_fingerprint = f"bedrock-{self.model_name.value}"
                async for chunk in response["stream"]:
                    formatted_chunk = self._format_chunk(
                        chunk, self.model_name.value, message_id, created_time, system_fingerprint
                    )
                    if formatted_chunk is not None:
                        yield json.dumps(formatted_chunk)
        except boto3.exceptions.Boto3Error as e:
            logger.error("Boto3 error during streaming: {}", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to stream content"
            )
        except Exception as e:
            logger.error("Unexpected error during streaming: {}", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to stream content"
            )
