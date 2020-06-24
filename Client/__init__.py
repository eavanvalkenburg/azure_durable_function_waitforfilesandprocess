import json
import logging
from dataclasses import dataclass
import azure.functions as func
import azure.durable_functions as df


@dataclass
class Blob:
    full_url: str
    file_name: str = None
    order_id: str = None
    file_type: str = None

    def __post_init__(self):
        self.file_name = self.full_url.split("/")[-1]
        self.order_id = self.file_name.split("-")[0]
        self.file_type = self.file_name.split("-")[1]


async def main(event: func.EventGridEvent, starter: str):
    client = df.DurableOrchestrationClient(starter)
    logging.info("Python EventGrid trigger processed an event: %s", event.get_json())
    blob = Blob(full_url=event.get_json()["url"])
    logging.info(f"Blob: {blob}")
    try:
        status = await client.get_status(blob.order_id)
        instance_id = status.instance_id
        logging.info("Got existing orchestrator, with instance id: %s", instance_id)
    except Exception:
        instance_id = await client.start_new("Orchestrator", blob.order_id, None)
        logging.info("Started new orchestration, with instance id: %s", instance_id)
    if instance_id:
        await client.raise_event(instance_id, blob.file_type, True)
    else:
        logging.error("Could not start orchestrator for instance: %s", blob.order_id)
