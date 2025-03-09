from fastapi import FastAPI

from models import TestAPIRequest, TestAPIResponse

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
