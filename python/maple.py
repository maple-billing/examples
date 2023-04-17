import datetime
import os
import rfc3339
import requests
import logging

from datetime import date

LOG_LEVEL = os.getenv("LOG_LEVEL")
logging.basicConfig(level=LOG_LEVEL)
log = logging.getLogger(__name__)

MAPLE_COMPANY_ID = os.getenv("MAPLE_COMPANY_ID")
MAPLE_API_KEY = os.getenv("MAPLE_API_KEY")
MAPLE_API_SERVER = os.getenv("MAPLE_API_SERVER")
MAPLE_EVENT_PATH = "/companies/" + MAPLE_COMPANY_ID + "/events/ingest"
MAPLE_EVENT_HEADERS = {"Authorization": "Bearer " + MAPLE_API_KEY}
MAPLE_ITEM_ID = "<ITEM_ID>"


def log_customer_event_to_maple(customer_event):
    event_data = [{
        "company_id": MAPLE_COMPANY_ID,
        "customer_identifier": customer_event.customer.id,
        "item_id": MAPLE_ITEM_ID,
        "transaction_id": customer_event.transaction_id,
        "timestamp": rfc3339.rfc3339(date.today()),
        "properties": {
            "quantity": customer_event.metric_quantity
        }
    }]

    # Post the event to maple billing
    path = MAPLE_API_SERVER + MAPLE_EVENT_PATH
    response = requests.post(path, json=event_data, headers=MAPLE_EVENT_HEADERS)
    log.debug("response from maple events: %d, %s", response.status_code, response.content)
