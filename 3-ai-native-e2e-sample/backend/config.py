import os

EVENT_HUBS_CONFIG = {
    "connection_string": os.getenv("EVENTHUB_CONNECTION_STRING"),
    "eventhub_name": os.getenv("EVENTHUB_NAME"),
    "consumer_group": os.getenv("CONSUMER_GROUP")
}
