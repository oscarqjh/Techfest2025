from crewai.tools import BaseTool
from typing import Type, List
from pydantic import BaseModel, Field
from .globals import client  # openai client
from . import LlmClient

"""
This is a tool that extracts data from a URL.

Returns:
    id: str
    
    content: str
    to_fact_check: bool
"""


class ArticleBodyItem(BaseModel):
    """Schema for each item in the article body"""

    id: str
    content: str
    to_fact_check: bool


class WebAnalyserInput(BaseModel):
    """Input schema for WebAnalyser"""

    data: dict


class WebAnalyserOutput(BaseModel):
    """Output schema for WebAnalyser"""

    article_body: List[ArticleBodyItem]
    topic: List[str]


class WebAnalyserTask(BaseTool):
    name: str = "WebAnalyser"
    description: str = "This tool analyses the content of a webpage"
    args_schema: Type[BaseModel] = WebAnalyserInput

    def _run(self, data: dict) -> dict:
        data = LlmClient.call_openai_api(data, "WebAnalyser")
        structured_data = WebAnalyserOutput(**data["web_analysis"])
        return structured_data.model_dump()
