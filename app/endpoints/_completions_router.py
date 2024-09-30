from typing import Union

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from loguru import logger
from openai.types.chat import ChatCompletion

from app.deps import authenticate_user
from app.schemas.completion_response import CompletionRequest
from app.services.not_diamond import get_not_diamond_response

router = APIRouter(
    prefix="/v1/completions",
    tags=["completions"],
)


@router.get(
    "/healthcheck",
    status_code=status.HTTP_200_OK,
)
def health_check():
    return {"status": "healthy"}


@router.post(
    "/",
    dependencies=[Depends(authenticate_user)],
    status_code=status.HTTP_200_OK,
    response_model=ChatCompletion,
)
def create_completion(
    completion_request: CompletionRequest,
) -> Union[ChatCompletion, StreamingResponse]:
    try:
        logger.info(f"Processing completion request: {completion_request}")
        return get_not_diamond_response(completion_request)
    except HTTPException as http_exc:
        logger.error(f"Failed to process completion: {http_exc}")
        raise http_exc
    except Exception as e:
        logger.error(f"Unexpected error processing completion: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process completion",
        )
