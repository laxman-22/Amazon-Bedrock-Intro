from fastapi import FastAPI
import boto3
import json
from botocore.exceptions import ClientError
from pydantic import BaseModel
import redis

app = FastAPI()
brt = boto3.client("bedrock-runtime")
rds =  redis.Redis(host="localhost", port=6379, decode_responses=True)

MODEL_ARN = "arn:aws:bedrock:us-east-2:381492212823:inference-profile/us.anthropic.claude-3-5-haiku-20241022-v1:0"

class Request(BaseModel):
    user_input: str
    session_id: str

# Chat function
@app.post('/chat')
def chat(req: Request):
    session_key = req.session_id

    messages = rds.get(session_key)
    if messages is not None:
        history = json.loads(messages)
    else:
        history = []
    
    history.append({
        "role": "user",
        "content": [{"type": "text", "text": req.user_input}]
    })

    request_payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "temperature": 0.5,
        "messages": history
    }

    try:
        response = brt.invoke_model(
            modelId=MODEL_ARN,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(request_payload)
        )
    except ClientError as e:
        return {"error": e}
    except Exception as e:
        return {"error": e}
    res = json.loads(response["body"].read())
    text = res["content"][0]["text"]
    history.append({
        "role": "assistant",
        "content": [{"type": "text", "text": text}]
    })
    rds.setex(session_key, 1800, json.dumps(history))
    return {"res": text}

# Clear Session method
@app.post("/clear")
def clear(req: Request):
    session_key = req.session_id
    rds.delete(session_key)
    return {"res": "success"}
