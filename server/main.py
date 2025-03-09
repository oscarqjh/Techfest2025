from fastapi import FastAPI
import json

from models import TestAPIRequest, TestAPIResponse, ValidationAPIRequest

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