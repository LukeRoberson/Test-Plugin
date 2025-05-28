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

from systemlog import system_log


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

# Initialize Flask application
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
    system_log.log(message=alert)
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
