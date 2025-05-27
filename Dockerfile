# Use the official Python image from the Docker Hub
FROM python:3.12-alpine
LABEL description="A simple test plugin for the AI assistant. This can be used to test the plugin system. Send webhooks with a browser, cURL, or Postman."
LABEL version="1.0.0"

# Create non-root user with no password
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Set the working directory in the container
WORKDIR /app

# Install uWSGI
RUN apk add --no-cache uwsgi-python3

# Change ownership of the application code to the non-root user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Entry point
CMD ["uwsgi", "--ini", "uwsgi.ini"]
