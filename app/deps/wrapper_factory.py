from fastapi import Depends, HTTPException, status

from app.interfaces import CompletionWrapper
from app.providers import AWSBedrockWrapper, ModelName, OpenAIWrapper

from .config import Settings, get_settings


def get_wrapper(settings: Settings = Depends(get_settings)) -> CompletionWrapper:
    if settings.foundation_model_name == ModelName.gpt_4o:
        return OpenAIWrapper(
            api_key=settings.openai_api_key,
            model=settings.foundation_model_name,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
        )
    elif settings.foundation_model_name in [ModelName.claude_sonnet_3, ModelName.claude_sonnet_3_5]:
        return AWSBedrockWrapper(
            region=settings.aws_bedrock_region,
            model_name=settings.foundation_model_name,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
        )
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid model name")
