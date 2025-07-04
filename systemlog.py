"""
Classes to manage system logs.
This sends logs to the logging service to manage.

Classes:
    SystemLog: Class to manage system logs.
        It can send logs to the logging service with default values.
"""

import logging
import requests
from datetime import datetime


class SystemLog:
    '''
    Class to manage system logs.
    Gets logs, and sends them to the logging service.

    Methods:
        __init__: Initialise the SystemLog class with default values.
        log: Send a log message to the logging service.
    '''

    def __init__(
        self,
        logging_url: str,
        source: str,
        destination: list,
        group: str,
        category: str,
        alert: str,
        severity: str,
    ) -> None:
        '''
        Initialise the SystemLog class.
        Values passed in here are default values. They can be overridden
            when sending a log.

        Args:
            logging_url (str): The URL of the logging service API.
            source (str): The source of the log message.
            destination (list): The destinations for the log message.
            group (str): The group to which the log message belongs.
            category (str): The category of the log message.
            alert (str): The alert type for the log message.
            severity (str): The severity level of the log message.

        Returns:
            None
        '''

        # Set up the default logging configuration
        self.url = logging_url
        self.source = source
        self.destination = destination
        self.group = group
        self.category = category
        self.alert = alert
        self.severity = severity

    def log(
        self,
        message: str,
        source: str = None,
        destination: list = None,
        group: str = None,
        category: str = None,
        alert: str = None,
        severity: str = None,
    ) -> bool:
        """
        Send a log message to the logging service.
        This requires just a message to send.
        Other parameters can be set. If not, default values will be used.

        Args:
            message (str): The log message to send.
            source (str): The source of the log message.
            destination (list): The destinations for the log message.
            group (str): The group to which the log message belongs.
            category (str): The category of the log message.
            alert (str): The alert type for the log message.
            severity (str): The severity level of the log message.

        Returns:
            bool: True if the log was sent successfully, False otherwise.
        """

        # Use default values if not provided
        source = source or self.source
        destination = destination or self.destination
        group = group or self.group
        category = category or self.category
        alert = alert or self.alert
        severity = severity or self.severity

        # Send a log as a webhook to the logging service
        try:
            result = requests.post(
                self.url,
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
                "Failed to send startup webhook to logging service. %s",
                e
            )
            return False

        # Check if the request was successful
        if result.status_code != 200:
            logging.error(
                "Failed to send log to logging service. "
                "Status code: %s, Response: %s",
                result.status_code,
                result.text
            )
            return False

        response_json = result.json()
        if response_json.get("result") != "success":
            logging.error(
                "Logging service did not return success. Response: %s",
                response_json
            )
            return False

        return True


# Initialize the SystemLog with default values
system_log = SystemLog(
    logging_url="http://logging:5100/api/log",
    source="webhook-plugin",
    destination=["web"],
    group="plugin",
    category="test webhook",
    alert="system",
    severity="info"
)
