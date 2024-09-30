import httpx
from loguru import logger

from app.deps.config import Settings


def _get_proposal_bid() -> float:
    """Get the bid amount for a proposal. This is a placeholder function that should be replaced
    with a real implementation. The idea is to calculate the bid amount based on:
    - The model's capabilities.
    - The instance requirements.
    - The running costs.
    - The estimated reward.
    """
    return 0.01


async def _create_proposal_for_instance(instance_id: str, settings: Settings) -> None:
    try:
        logger.info(f"Creating proposal for instance id: {instance_id}")
        proposal_max_bid = _get_proposal_bid()
        logger.info(
            f"Creating proposal with bid amount: {proposal_max_bid}, for instance: {instance_id}"
        )
        headers = {
            "x-api-key": settings.market_api_key,
            "Accept": "application/json",
        }
        url = f"{settings.market_url}/v1/proposals/create/for-instance/{instance_id}"
        data = {
            "endpoint": settings.app_completions_endpoint,
            "max_bid": proposal_max_bid,
            "endpoint_api_key": settings.app_api_key,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
        response.raise_for_status()
        logger.info(f"Proposal for instance id {instance_id} created successfully")
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")


async def fill_open_instances_in_market(settings: Settings) -> None:
    try:
        headers = {
            "x-api-key": settings.market_api_key,
            "Accept": "application/json",
        }
        url = f"{settings.market_url}/v1/instances/"
        params = {"instance_status": settings.market_open_instance_code}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        open_instances = response.json()

        if not open_instances:
            return

        url = f"{settings.market_url}/v1/proposals/"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
        response.raise_for_status()
        proposals = response.json()

        filled_instances = set(proposal["instance_id"] for proposal in proposals)
        unfilled_instances = [
            instance for instance in open_instances if instance["id"] not in filled_instances
        ]
        for instance in unfilled_instances:
            logger.info(f"Processing instance: {instance}")
            await _create_proposal_for_instance(instance["id"], settings)
    except Exception as e:
        logger.error("Unexpected error occurred: {}", e)
