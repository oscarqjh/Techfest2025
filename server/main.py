from fastapi import FastAPI
import json

from pydantic import BaseModel
from models import TestAPIRequest, TestAPIResponse, ValidationAPIRequest
import sys
from pathlib import Path


# Dynamically determine the path
project_root = Path(__file__).resolve().parent.parent
rurl_flow_path = project_root / 'rurl_flow' / 'src' / 'rurl_flow'
sys.path.append(str(rurl_flow_path))


class CredibilityRequest(BaseModel):
    url: str

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/api/v1/helloworld")
def hello_world():
    return {"message": "Hello, World!"}

@app.post("/api/v1/test")
def test_endpoint(data: TestAPIRequest) -> TestAPIResponse:
    print(data)
    return {"message": "Test successful!"}

@app.post("/api/v1/validate")
def validate_endpoint(data: ValidationAPIRequest):
    print(data)
    return {"message": "Validation successful!"}

@app.get("/sample_output")
def sample_output():
    with open("./results.json", "r") as file:
        parsed_data = json.load(file)
    return parsed_data

@app.post("/analyse_credibility")
def analyse_credibility(data: CredibilityRequest):
    from main import kickoff
    url = data.url
    res = kickoff(url=url)

    return res
