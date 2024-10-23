
# Docker Meal Tracker Demo Api Python
API to serve as a simple demo to showcase login and meal tracking functionality.

## Table of Contents
1. [Initial Setup](#initial-setup)
   - [Setup Repository](#setup-repository)
   - [Create Required Directories](#create-required-directories)
   - [Copy Template Files](#copy-template-files)
   - [Edit Configuration](#edit-configuration)

2. [Local Deployment for Testing and Debugging](#local-deployment-for-testing-and-debugging)
   - [Docker Compose Build](#docker-compose-build)

3. [Production Deployment](#production-deployment)
   - [Build Docker Image](#build-docker-image)
   - [Push to Docker Hub](#push-to-docker-hub)
   - [Deploy Using Docker Swarm](#deploy-using-docker-swarm)

## Initial Setup

### Setup Repository
Clone the repository to your local machine:

```bash
mkdir -p /path/to/api/directory/meal-tracker-api-python
cd /path/to/api/directory/meal-tracker-api-python
git clone https://github.com/yourusername/meal-tracker-api-python.git .
```

### Copy Template Files
Once the repository is cloned, copy the template files to the appropriate locations:

```bash
cp config.txt.template config.txt
cp .env.template .env
```

### Edit Configuration
Edit the copied template files to set up your environment variables and configuration:

- **config.txt**: Configure your database, API settings, etc.
- **.env**: Set up environment variables such as database credentials and API keys.

## Local Deployment for Testing and Debugging

### Docker Compose Build
To deploy the API locally for testing and debugging, use Docker Compose to build and run the container:

```bash
docker compose -f /path/to/docker-compose.yml up
```

This is recommended only for development purposes. Ensure that your local configuration is correctly set up in the `.env` and `config.txt` files before running the command.

## Production Deployment

For production deployment, it is recommended to build the Docker image, push it to Docker Hub, and deploy using Docker Swarm.

### Build Docker Image
Build the Docker image using the following command:

```bash
docker build -t yourdockerhubusername/meal-tracker-api-python:latest .
```

### Push to Docker Hub
Once the image is built, push it to your Docker Hub repository:

```bash
docker push yourdockerhubusername/meal-tracker-api-python:latest
```

### Deploy Using Docker Swarm
Deploy the API in a Docker Swarm cluster by pulling the image from Docker Hub:

```bash
docker service create --name meal-tracker-api-python --replicas 3 --publish 8080:8080 yourdockerhubusername/meal-tracker-api-python:latest
```

Make sure your `.env` and configuration files are properly set up before deploying the service.
