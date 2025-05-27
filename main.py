"""
Test webhook plugin

Uses Flask to create a simple web application that listens
    for incoming webhook requests.

Usage:
    Run this module to start the web application.

Example:
    $ python main.py

Example webhook body that this might receive (JSON):
    {
        "type": "example.event",
        "timestamp": "2022-11-03T20:26:10.344522Z",
        "data": {
            "foo": "bar",
            "fizzbuzz": 2
        }
    }

Webhook format that this would send (JSON) to the logging service:
    {
        "source": "<PLUGIN-NAME>",
        "type": "<EVENT>",
        "timestamp": "<DATE-AND-TIME>",
        "message": "<MESSAGE STRING>"
    }

Plugin parses and filters the incoming webhook request,
    and sends a formatted message to the logging service.
"""

from flask import Flask, request
import requests
import logging


# Set up logging
logging.basicConfig(level=logging.INFO)

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
    response = requests.post(
        "http://logging:5100/api/webhook",
        json=alert
    )
    logging.info(
        "Sent alert to logging service: %s",
        response.status_code
    )

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
