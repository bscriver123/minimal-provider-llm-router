from typing import Optional, Self

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings

from app.providers import ModelName


class Settings(BaseSettings):
    foundation_model_name: ModelName = Field(..., description="The name of the model to use.")

    aws_bedrock_region: Optional[str] = Field(None, description="The AWS region.")

    openai_api_key: Optional[str] = Field(None, description="The API key for OpenAI.")

    app_api_key: str = Field(..., description="The API key for the application.")
    app_completions_endpoint: str = Field(..., description="The endpoint for completions.")

    agent_market_url: str = Field(
        "https://api.agent.market", description="The URL for the agent market."
    )
    agent_market_api_key: str = Field(..., description="The API key for the agent market.")
    agent_market_scan_interval: int = Field(
        2, gt=0, description="The interval in seconds at which to scan the agent market."
    )
    agent_market_open_instance_code: int = Field(
        0, description="The code for an open instance in the agent market."
    )

    web_port: int = Field(80, description="The port on which the web server runs.")
    max_bid: float = Field(0.01, gt=0, description="The maximum bid for a proposal.")
    temperature: float = Field(
        0.9,
        gt=0,
        lt=1,
        description="The temperature setting for the model, must be between 0 and 1.",
    )
    max_tokens: int = Field(
        1000,
        gt=0,
        description="The maximum number of tokens to generate, must be a positive integer.",
    )

    class Config:
        case_sensitive = False

    @model_validator(mode="after")
    def check_keys(self) -> Self:
        if self.foundation_model_name in [ModelName.claude_sonnet_3, ModelName.claude_sonnet_3_5]:
            if not self.aws_bedrock_region:
                raise ValueError(
                    "AWS access key ID, secret access key and region are required for AWS models."
                )
        elif self.foundation_model_name in [ModelName.gpt_4o]:
            if not self.openai_api_key:
                raise ValueError("OpenAI API key is required for OpenAI models.")
        else:
            raise ValueError("Invalid model name")
        return self


settings = Settings()


def get_settings():
    return settings
