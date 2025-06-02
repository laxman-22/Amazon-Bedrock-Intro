# Amazon Bedrock Intro

This repository contains the code that allows a user to interact with a model (Claude 3.5 Haiku) using Amazon Bedrock, Redis (for memory), and FastAPI (for the endpoint).

## Code Structure

* The code uses a very simple design pattern to make requests to Amazon Bedrock, there are 2 endpoints ```/chat``` and ```/clear```
* The structure of each requests is also straightforward, in the body of each request is a JSON that looks like this:
```
{
  "user_input": "what is the capital of france?",
  "session_id": "1"
}
```
* For a new session, simply put a different number for session_id, and to change the prompt, change user_input.
* For context management, requests are all stored in Redis, so for a particular session once a question is asked, the subsequent questions will take the previous context into account, retaining both the prompt and the response while also not interfering with other sessions.

## Installation and Usage

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
```(bash)
pytest --cov=. test_suite.py 
```