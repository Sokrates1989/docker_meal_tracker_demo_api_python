
# Docker Meal Tracker API Demo (Python)

This API serves as a **demonstration** for user authentication and meal tracking functionalities, designed for **evaluation purposes only**. It allows users to register, log in, and perform CRUD operations on meals using Docker for containerized deployment. This demo is not intended for production use and is provided under an **Evaluation License**.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Initial Setup](#initial-setup)
    - [Cloning the Repository](#cloning-the-repository)
    - [Setting Up Configuration](#setting-up-configuration)
3. [Local Deployment for Development](#local-deployment-for-development)
    - [Building with Docker Compose](#building-with-docker-compose)
4. [Production Deployment](#production-deployment)
    - [Building the Docker Image](#building-the-docker-image)
    - [Pushing to Docker Hub](#pushing-to-docker-hub)
    - [Deploying with Docker Swarm](#deploying-with-docker-swarm)
5. [Documentation](#documentation)
    - [Viewing Documentation Online](#viewing-documentation-online)
    - [Generating API Documentation](#generating-api-documentation)
    - [Integrate this README into the documentation](#manual-integration-of-readmemd) 
6. [License](#license)

---

## Project Overview

This demo API provides basic functionality for meal tracking, including user authentication and meal management. Built using FastAPI and MySQL, it supports operations such as registering users, logging in, and managing meal data (adding, editing, deleting meals). The project leverages Docker for seamless deployment in both local and production environments.

This project is designed **for evaluation purposes only** and should not be used in a production environment.

### Key Features

- **User Authentication:** Register and log in users with token-based authentication.
- **Meal Tracking:** Add, edit, and delete meals.
- **Containerized Deployment:** Docker Compose for local development and Docker Swarm for production deployment.

---

## Initial Setup

### Cloning the Repository

First, clone the repository to your local environment:

```bash
mkdir -p /path/to/api/directory/meal-tracker-api-python
cd /path/to/api/directory/meal-tracker-api-python
git clone https://github.com/yourusername/meal-tracker-api-python.git .
```

### Setting Up Configuration

After cloning, copy the template configuration files to the appropriate locations:

```bash
cp config.txt.template config.txt
cp .env.template .env
```

Edit these files to configure your environment variables:

- **config.txt:** Configure your database settings, encryption keys, and other API-related settings.
- **.env:** Set up sensitive environment variables like database credentials and API tokens.

---

## Local Deployment for Development

### Building with Docker Compose

To deploy the API locally for development and testing, use Docker Compose to build and run the container:

```bash
docker-compose -f /path/to/docker-compose.yml up
```

Make sure that the `.env` and `config.txt` files are correctly configured before running the command. This setup is recommended for local development only.

---

## Production Deployment

For production, we recommend building the Docker image, pushing it to Docker Hub, and deploying the service using Docker Swarm.

### Building the Docker Image

Build the Docker image locally using the following command:

```bash
docker build -t yourdockerhubusername/meal-tracker-api-python:latest .
```

### Pushing to Docker Hub

Once the image is built, push it to your Docker Hub repository:

```bash
docker push yourdockerhubusername/meal-tracker-api-python:latest
```

### Deploying with Docker Swarm

To deploy the API on a Docker Swarm cluster, pull the image from Docker Hub and create a service:

```bash
docker service create --name meal-tracker-api-python --replicas 3 --publish 8080:8080 yourdockerhubusername/meal-tracker-api-python:latest
```

Ensure that your `.env` and configuration files are properly set up before deploying the service in production.

---

## Documentation

### Viewing Documentation Online

An online version of the project's internal developer documentation can be found at:  
[https://api-python-doku.engaige.fe-wi.com/](https://api-python-doku.engaige.fe-wi.com/)

### Generating API Documentation

To generate the project's documentation locally, follow these steps:

#### 1. Use Docker Compose to Generate Documentation
Instead of manually installing dependencies on your system, you can use the provided Docker Compose setup to generate the documentation automatically.

#### Build the Docker Container for Documentation Generation:

In the root directory of the project, run the following command:

```bash
docker-compose -f docker-compose-create-doc.yml up
```

This will build and run a container that generates the documentation inside the docs/ folder of your project. The DOCKERFILE-CREATE-DOCU Dockerfile defines how the container is built, including all dependencies like pdoc3.

#### 2. Locate the Generated HTML Files:
- The API documentation will be located in docs/index.html.
- The README.md will be converted into docs/readme.html.

#### 3. Insert the Converted README Content:
Open the docs/index.html file and manually copy the HTML content from readme.html into the appropriate section in index.html.

---

## License

This software is provided under an **Evaluation License Agreement**. It may only be used for evaluation purposes and cannot be modified, copied, or distributed without the express permission of the author.

For full details, please refer to the [LICENSE](./LICENSE) file.
