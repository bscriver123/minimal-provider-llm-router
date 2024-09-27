from typing import Optional

from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class CompletionRequest(BaseModel):
    messages: list[dict]

    class Config:
        extra = "allow"


class Choice(BaseModel):
    index: int
    message: Message
    logprobs: Optional[dict]
    finish_reason: str


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
