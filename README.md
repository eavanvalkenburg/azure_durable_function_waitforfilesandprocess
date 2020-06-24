# Azure Durable Function - Python sample 

A set of python functions built on [the preview](https://github.com/Azure/azure-functions-durable-python/tree/dev) that waits for three types of events, processes them, and finally writes them to CosmosDB. Triggered by Event Grid.

### Client
The Client is the actual listener for events, it is triggered by an [Event Grid Event](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-event-grid-trigger?tabs=python), and uses the information in it to decide which instance this is and raises an event on that instance of a type that matches the incoming event.

### Orchestrator
The orchestrator has the main logic, it creates three tasks for the three different event types and waits for the events associated with those, once all three events have taken place it starts the next two activities.

### CombineFiles
This activity takes the completed set of files and sends a call to a external API that has the logic for combining the files, it returns that logic to the Orchestrator.

### SendToCosmos
This activity takes the dict it gets and sends that to CosmosDB using the [outgoing CosmosDB binding](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-cosmosdb-v2-output?tabs=python).