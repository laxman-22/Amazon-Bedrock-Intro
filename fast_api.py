from fastapi import FastAPI
import boto3
import json
from botocore.exceptions import ClientError

app = FastAPI()
brt = boto3.client("bedrock-runtime")

MODEL_ARN = "arn:aws:bedrock:us-east-2:381492212823:inference-profile/us.anthropic.claude-3-5-haiku-20241022-v1:0"
prompt = "describe what your capabilities are briefly"

request_payload = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 512,
    "temperature": 0.5,
    "messages": [
        {
            "role": "user",
            "content": [{"type": "text", "text": prompt}],
        }
    ],
}


@app.get('/hello')
def read():
    try:
        response = brt.invoke_model(
            modelId=MODEL_ARN,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(request_payload)
        )
    except(ClientError, Exception) as e:
        print(e)
        exit(1)
    res = json.loads(response["body"].read())
    text = res["content"][0]["text"]
    print(text)
    return text
