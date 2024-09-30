import time

from loguru import logger
from notdiamond import NotDiamond
from openai.types.chat import ChatCompletion

from app.schemas.completion_response import CompletionRequest

not_diamond_client = NotDiamond()


def get_not_diamond_response(completion_request: CompletionRequest) -> ChatCompletion:
    result, session_id, provider = not_diamond_client.chat.completions.create(
        messages=completion_request.messages,
        model=[
            "openai/gpt-4o",
            "openai/gpt-4o-mini",
            "anthropic/claude-3-opus-20240229",
            "anthropic/claude-3-5-sonnet-20240620",
            "anthropic/claude-3-haiku-20240307",
        ],
        tradeoff="cost",
    )

    logger.info(
        f"Notdiamond called LLM: {provider.model} with the completion_request: {completion_request}"
    )  # noqa

    return ChatCompletion(
        id=result.id,
        object="chat.completion",
        created=int(time.time()),
        model=result.response_metadata["model_name"],
        usage=result.response_metadata["token_usage"],
        choices=[
            {
                "message": {
                    "role": "assistant",
                    "content": result.content,
                },
                "logprobs": result.response_metadata["logprobs"],
                "finish_reason": result.response_metadata["finish_reason"],
                "index": 0,
            },
        ],
    )
