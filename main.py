"""
Test webhook plugin

Uses Flask to create a simple web application that listens
    for incoming webhook requests.

Plugin parses and filters the incoming webhook request,
    and sends a formatted message to the logging service.
"""

from flask import Flask, request
import requests
import logging
from datetime import datetime


# Get global config
global_config = None
try:
    response = requests.get("http://web-interface:5100/api/config", timeout=3)
    response.raise_for_status()  # Raise an error for bad responses
    global_config = response.json()

except Exception as e:
    logging.critical(
        "Failed to fetch global config from web interface."
        f" Error: {e}"
    )

if global_config is None:
    raise RuntimeError("Could not load global config from web interface")

# Set up logging
log_level_str = global_config['config']['web']['logging-level'].upper()
log_level = getattr(logging, log_level_str, logging.INFO)
logging.basicConfig(level=log_level)
logging.info("Logging level set to: %s", log_level_str)


def send_log(
    message: str,
    url: str = "http://logging:5100/api/log",
    source: str = "test-plugin",
    destination: list = ["web"],
    group: str = "plugin",
    category: str = "test",
    alert: str = "event",
    severity: str = "info",
) -> None:
    """
    Send a message to the logging service.

    Args:
        message (str): The message to send.
        url (str): The URL of the logging service API.
        source (str): The source of the log message.
        destination (list): The destinations for the log message.
        group (str): The group to which the log message belongs.
        category (str): The category of the log message.
        alert (str): The alert type for the log message.
        severity (str): The severity level of the log message.
    """

    # Send a log as a webhook to the logging service
    try:
        requests.post(
            url,
            json={
                "source": source,
                "destination": destination,
                "log": {
                    "group": group,
                    "category": category,
                    "alert": alert,
                    "severity": severity,
                    "timestamp": str(datetime.now()),
                    "message": message
                }
            },
            timeout=3
        )
    except Exception as e:
        logging.warning(
            "Failed to send log to logging service. %s",
            e
        )


app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    # Parse the incoming webhook request
    data = request.get_json()
    alert = {
        "source": "Test Plugin",
        "destination": ["web"],
        "log": {
            "type": data['type'],
            "timestamp": data["timestamp"],
            "message": (
                f"Foo: {
                    data['data']['foo']
                }, FizzBuzz: {
                    data['data']['fizzbuzz']
                }"
            )
        }
    }

    # Debug - print the alert
    logging.info("Parsed alert: %s", alert)

    # Send the alert to the logging service
    send_log(message=alert)
    logging.info("Sent alert to logging service: %s")

    return "Received", 200


'''
NOTE: When running in a container, the host and port are set in the
    uWSGI config. uWSGI starts the process, which means the
    Flask app is not run directly.
    This can be uncommented for local testing.
'''
# if __name__ == "__main__":
#     app.run(
#         debug=True,
#         port=5000
#     )
