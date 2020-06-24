# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import azure.functions as func


async def main(doc: tuple, outdoc: func.Out[func.Document]) -> bool:
    instance, doc = doc
    logging.info("%s: Starting SendToCosmos function with data: %s", instance, doc)
    try:
        outdoc.set(func.Document.from_dict(doc))
        return True
    except Exception:
        return False
