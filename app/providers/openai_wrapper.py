import json
from typing import AsyncGenerator

from fastapi import HTTPException, status
from loguru import logger
from openai import APIConnectionError, APIError, AsyncOpenAI, OpenAIError
from openai.types.chat import ChatCompletion


class OpenAIWrapper:
    def __init__(self, api_key: str, model: str, temperature: float, max_tokens: int):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self.system_prompt = "You are a helpful assistant."
        self.temperature = temperature
        self.max_tokens = max_tokens

    async def create_completion(self, messages: list[dict[str, str]]) -> ChatCompletion:
        try:
            messages = self._add_system_message(messages, self.system_prompt)
            return await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
        except (APIError, APIConnectionError) as e:
            logger.error("OpenAI API error: {}", e)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="OpenAI service unavailable or connection issue",
            )
        except OpenAIError as e:
            logger.error("OpenAI error: {}", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
            )
        except Exception as e:
            logger.error("Unexpected error processing completion: {}", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
            )

    @staticmethod
    def _add_system_message(
        messages: list[dict[str, str]], system_prompt: str
    ) -> list[dict[str, str]]:
        return [{"role": "system", "content": system_prompt}] + messages

    async def get_stream_content(self, messages: list[dict[str, str]]) -> AsyncGenerator[str, None]:
        try:
            messages = self._add_system_message(messages, self.system_prompt)
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=True,
            )
            async for chunk in response:
                yield json.dumps(chunk.dict())
        except (APIError, APIConnectionError) as e:
            logger.error("OpenAI API error: {}", e)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="OpenAI service unavailable or connection issue",
            )
        except OpenAIError as e:
            logger.error("OpenAI error: {}", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
            )
        except Exception as e:
            logger.error("Unexpected error processing completion: {}", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
            )
