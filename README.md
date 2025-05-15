# Overview

A very simple test plugin.

Receives webhooks from an external source, such as Postman, and prints them to the screen.

Uses Flask as the web server to receive the webhooks.

Everything runs from main.py.


## Modules

| Module   | Usage                                 |
| -------- | ------------------------------------- |
| Flask    | Web framework                         |
| Requests | Send API calls to the logging service |



</br></br>
---

# Logging Service
The plugin will send information to the logging service. This is an REST API call:

POST /api/webhook

The body of the POST contains relevant information in a standard format. The logging service receives this, and decides what to do from there.

This is connectionless. The plugin is not concerned if the logging service receives or acknowledges this.


</br></br>
---

# Sample Webhook
## Incoming Webhooks
This is how an incoming webhook might look

Method: POST

Data Type: JSON

Body:

{
  "type": "example.event",
  "timestamp": "2022-11-03T20:26:10.344522Z",
  "data": {
    "foo": "bar",
    "fizzbuzz": 2
  }
}


## Outbound Webhook
The plugin needs to parse the information into a standard format before sending to the logging service.

This is how the outbound webhook is formatted:

Body:

{
    "source": "<PLUGIN-NAME>",
    "type": "<EVENT>",
    "timestamp": "<DATE-AND-TIME>",
    "message": "<MESSAGE STRING>"
}
