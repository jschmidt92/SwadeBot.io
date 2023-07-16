FROM alpine

# Set work directory
WORKDIR /app

# Mount the api volume
VOLUME /api

# Install dependencies
RUN apk add --update --no-cache python3 py3-pip

# Copy project
COPY . /app

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Run the application:
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Define the stop signal
STOPSIGNAL SIGINT