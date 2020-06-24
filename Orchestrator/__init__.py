# This function is not intended to be invoked directly. Instead it will be
# triggered by an HTTP starter function.
# Before running this sample, please:
# - create a Durable activity function (default name is "Hello")
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import json
import azure.functions as func
import azure.durable_functions as df


def orchestrator_function(context: df.DurableOrchestrationContext) -> bool:
    logging.debug("Running orchestrator: %s", context.instance_id)
    inst_id = context.instance_id
    expected_files = [
        "OrderHeaderDetails.csv",
        "OrderLineItems.csv",
        "ProductInformation.csv",
    ]
    events = [context.wait_for_external_event(file) for file in expected_files]
    events_result = yield context.task_all(events)

    logging.info("%s, Event results: %s", inst_id, events_result)
    logging.info(
        "%s: All events should have happened, running CombineFiles and SendToCosmos.",
        inst_id,
    )
    json_doc = yield context.call_activity("CombineFiles", inst_id)
    logging.info(
        "%s: CombineFiles has come back with %s", inst_id, json_doc,
    )
    result = yield context.call_activity("SendToCosmos", (inst_id, json_doc))
    logging.info("%s: SendToCosmos has come back with %s", inst_id, result)
    return result


main = df.Orchestrator.create(orchestrator_function)
