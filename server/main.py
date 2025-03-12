from fastapi import FastAPI
import json

from pydantic import BaseModel
from models import TestAPIRequest, StoreDataRequest, TestAPIResponse, ValidationAPIRequest, CredibilityRequest, GetNewsRequest
import sys
from pathlib import Path




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
    return json.dumps(parsed_data)

@app.post("/analyse_credibility")
def analyse_credibility(data: CredibilityRequest):
    from rurl_flow.src.rurl_flow.main import RunFlow
    url = data.url
    llm = data.llm # "gpt" or "groq"
    res = RunFlow().kickoff(url=url, llm=llm)

    return res

@app.post("/get_news")
def get_news(data: GetNewsRequest):
    from rurl_flow.src.rurl_flow.tools.web_parsing_tool import WebParsingTool
    parser = WebParsingTool()
    url = data.url
    res = parser.run(url=url)
    return res

@app.post("/store_data")
def store_data(req: StoreDataRequest):
    from neondb.apis.rurldata_api import insert_one_rurldata
    print(req)
    insert_one_rurldata(json.dumps(req.data))
    return {"message": "Data stored successfully!"}

@app.get("/get_data")
def get_data():
    from neondb.apis.rurldata_api import get_one_rurldata
    data = get_one_rurldata()
    return data
