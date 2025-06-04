# Use the custom base image
FROM lukerobertson19/base-os:latest
LABEL description="A simple test plugin for the AI assistant. This can be used to test the plugin system. Send webhooks with a browser, cURL, or Postman."
LABEL version="1.0.0"

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Start the application using uWSGI
CMD ["uwsgi", "--ini", "uwsgi.ini"]
