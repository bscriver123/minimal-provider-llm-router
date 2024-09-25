import httpx
from loguru import logger

from app.deps.config import Settings


async def _create_proposal_for_instance(instance_id: str, settings: Settings) -> None:
    try:
        logger.info("Creating proposal for instance id: {}", instance_id)

        headers = {
            "x-api-key": settings.agent_market_api_key,
            "Accept": "application/json",
        }
        url = f"{settings.agent_market_url}/v1/proposals/create/for-instance/{instance_id}"
        data = {
            "endpoint": settings.app_completions_endpoint,
            "max_bid": settings.max_bid,
            "endpoint_api_key": settings.app_api_key,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
        response.raise_for_status()
        logger.info("Proposal created successfully")
    except AttributeError as e:
        logger.error("Settings attribute error: {}", e)
    except httpx.HTTPStatusError as e:
        logger.error("HTTP error occurred: {}", e)
    except httpx.RequestError as e:
        logger.error("Request error occurred: {}", e)
    except Exception as e:
        logger.error("Unexpected error occurred: {}", e)


async def fill_open_instances_in_agent_market(settings: Settings) -> None:
    try:
        headers = {
            "x-api-key": settings.agent_market_api_key,
            "Accept": "application/json",
        }
        url = f"{settings.agent_market_url}/v1/instances/"
        params = {"instance_status": settings.agent_market_open_instance_code}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        open_instances = response.json()

        if not open_instances:
            return

        url = f"{settings.agent_market_url}/v1/proposals/"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
        response.raise_for_status()
        proposals = response.json()

        filled_instances = set(proposal["instance_id"] for proposal in proposals)
        unfilled_instances = [
            instance for instance in open_instances if instance["id"] not in filled_instances
        ]
        for instance in unfilled_instances:
            logger.info("Processing instance: {}", instance)
            await _create_proposal_for_instance(instance["id"], settings)
    except AttributeError as e:
        logger.error("Settings attribute error: {}", e)
    except httpx.HTTPStatusError as e:
        logger.error("HTTP error occurred: {}", e)
    except httpx.RequestError as e:
        logger.error("Request error occurred: {}", e)
    except ValueError as e:
        logger.error("JSON decode error occurred: {}", e)
    except Exception as e:
        logger.error("Unexpected error occurred: {}", e)
