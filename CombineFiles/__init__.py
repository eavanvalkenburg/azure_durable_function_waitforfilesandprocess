# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import aiohttp
import asyncio
import os

url = os.environ["CombineURL"]
headers = {"Content-Type": "application/json"}


async def main(orderid: str) -> str:
    instance = orderid
    logging.info(
        "%s: Starting CombineFiles function with order_id: %s", instance, orderid
    )
    body = {
        "orderHeaderDetailsCSVUrl": f"{orderid}-orderHeaderDetails.csv",
        "orderLineItemsCSVUrl": f"{orderid}-OrderLineItems.csv",
        "productInformationCSVUrl": f"{orderid}-ProductInformation.csv",
    }
    logging.info("%s: Body to be sent: %s", instance, body)
    async with aiohttp.ClientSession(raise_for_status=False) as session:
        async with session.post(url, headers=headers, json=body) as response:
            try:
                resp = await response.json()
            except Exception:
                resp = {"headers": {"locationId": "test"}, "order_id": orderid}
    logging.info("%s: CombineFiles response: %s", instance, resp)
    return resp
