from typing import Any, AsyncGenerator, Protocol


class CompletionWrapper(Protocol):
    async def create_completion(self, messages: list[dict[str, str]]) -> Any:
        ...

    async def get_stream_content(self, messages: list[dict]) -> AsyncGenerator[dict, None]:
        ...
