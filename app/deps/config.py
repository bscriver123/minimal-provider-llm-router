from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str = Field(..., description="The API key for OpenAI.")
    anthropic_api_key: str = Field(..., description="The API key for Anthropic.")
    notdiamond_api_key: str = Field(..., description="The API key for notdiamond.")

    app_api_key: str = Field(..., description="The API key for the application.")
    app_completions_endpoint: str = Field(..., description="The endpoint for completions.")

    market_url: str = Field("https://api.marketrouter.ai", description="The market URL.")
    market_api_key: str = Field(..., description="The market API key.")
    market_scan_interval: int = Field(
        2, gt=0, description="The interval in seconds at which to scan the market."
    )
    market_open_instance_code: int = Field(
        0, description="The code for an open instance in the market."
    )

    web_port: int = Field(80, description="The port on which the web server runs.")
    max_tokens: int = Field(
        1000,
        gt=0,
        description="The maximum number of tokens to generate, must be a positive integer.",
    )

    class Config:
        case_sensitive = False


settings = Settings()


def get_settings():
    return settings
