AI Deployment Guide

This guide provides instructions for deploying the project, which includes a Flask application for performing predictions using TinyBERT, along with Redis and RabbitMQ for caching and asynchronous processing, respectively.
### Prerequisites

    Docker: Make sure you have Docker installed on your system. You can download and install Docker from here.

### Deployment Steps

    Clone the Repository: Clone this repository to your local machine.

    

```git clone <repository_url>```

Navigate to Project Directory: Change your current directory to the root directory of the cloned repository.



```cd <project_directory>```

Update Configuration: Edit the config.json file located in the app directory to specify the hostnames and ports for Redis and RabbitMQ if necessary.

Build and Start Docker Containers: Run the following command to build and start the Docker containers defined in the docker-compose.yml file.



    ```docker-compose up --build```

This command will build the Docker image for the Flask application and start the containers for Flask, Redis, and RabbitMQ.

Access the Application: Once the containers are up and running, you can access the Flask application by navigating to http://localhost:8000 in your web browser.

Perform Predictions: To perform predictions using the Flask application, send POST requests to http://localhost:8000/predict with JSON payload {"text": "Your input text here"}.

### Additional Notes

The Flask application listens on port 8000 by default. You can modify the port in the docker-compose.yml file if needed.

Redis is used for caching predictions, and RabbitMQ is used for asynchronous processing of requests. Make sure these services are running and accessible to the Flask application.

For production deployments, consider securing your application, setting up logging and monitoring, and optimizing performance as needed.
