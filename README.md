# Amazon-Bedrock-Intro

This repository contains the code that allows a user to interact with a model using Amazon Bedrock, Redis (for memory), and FastAPI (for the endpoint).

## Installation

1) Clone this repo locally onto your machine
```(bash)
git clone https://github.com/laxman-22/Amazon-Bedrock-Intro.git
```
2) Install the [AWS CLI](https://aws.amazon.com/cli/)
3) You need an access key and a secret access key that you must set with the following command
```(bash)
aws configure
```
4) Install [Docker](https://docs.docker.com/desktop/setup/install/windows-install/) (to run the Redis container for memory management and maintaining context)

5) Run the Docker image
```(bash)
docker run -d -p 6379:6379 redis
```
6) Install all dependencies
```(bash)
pip install -r requirements.txt
```
7) Start the FastAPI server
```(bash)
uvicorn fast_api:app --reload
```

8) Use Postman to make requests to the Amazon Bedrock model via the FastAPI endpoints (ensure payloads are in the Body of each request and they are in a JSON format)

9) In order to run the testing suite, keep the Docker image running and run the test code