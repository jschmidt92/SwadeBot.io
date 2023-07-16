FROM node:alpine

# Set work directory
WORKDIR /app

# Mount the app volume
VOLUME /app

# Copy package.json
COPY ./package*.json /app

# Install dependencies
RUN npm install

# Copy project
COPY . /app

# Run the application:
CMD ["npm", "run", "dev"]

# Define the stop signal
STOPSIGNAL SIGINT
