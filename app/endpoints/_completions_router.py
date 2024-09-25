from typing import Union

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from loguru import logger
from openai.types.chat import ChatCompletion

from app.deps import authenticate_user, get_wrapper
from app.interfaces import CompletionWrapper
from app.schemas.completion_response import CompletionRequest

router = APIRouter(
    prefix="/v1/completions",
    tags=["completions"],
)


@router.get(
    "/healthcheck",
    status_code=status.HTTP_200_OK,
)
async def health_check():
    return {"status": "healthy"}


@router.post(
    "/",
    dependencies=[Depends(authenticate_user)],
    status_code=status.HTTP_200_OK,
    response_model=ChatCompletion,
)
async def create_completion(
    completion_request: CompletionRequest,
    wrapper: CompletionWrapper = Depends(get_wrapper),
) -> Union[ChatCompletion, StreamingResponse]:
    try:
        logger.info("Processing completion request: {}", completion_request)
        if completion_request.model_dump().get("stream"):
            logger.debug("Streaming completion")
            streaming_response = StreamingResponse(
                wrapper.get_stream_content(completion_request.messages),
                media_type="application/json",
            )
            logger.debug("Streaming completion processed successfully")
            return streaming_response
        else:
            logger.debug("Non-stream completion")
            conversation = await wrapper.create_completion(completion_request.messages)
            logger.debug("Completion processed successfully")
            return conversation
    except HTTPException as http_exc:
        logger.error("Failed to process completion: {}", http_exc)
        raise http_exc
    except Exception as e:
        logger.error("Unexpected error processing completion: {}", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process completion",
        )
