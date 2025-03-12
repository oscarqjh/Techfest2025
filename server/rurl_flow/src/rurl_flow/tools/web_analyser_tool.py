from crewai.tools import BaseTool
from typing import Type, List, Union
from pydantic import BaseModel
from .globals import client  # OpenAI client
from . import llm_client
import re
import json

"""
This is a tool that extracts data from a URL.

Returns:
    article_body: List[ArticleBodyItem]
    topic: List[str]
    entities: List[str]  
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
    entities: List[Union[str, dict]]


class WebAnalyserTool(BaseTool):
    """Tool for analyzing webpage content"""

    name: str = "WebAnalyser"
    description: str = (
        "This tool analyses the content of a webpage and extracts key insights."
    )
    args_schema: Type[BaseModel] = WebAnalyserInput

    def _run(self, data: dict, llm) -> dict:
        """Runs the web analysis tool and returns structured output"""
        try:
            data = llm_client.call_openai_api(data, "WebAnalyser", llm_model=llm)
            
            try:
                # Remove Markdown code block markers 
                print("LOL")
                clean_text = re.sub(r"```json|```", "", data["web_analysis"]).strip()
                parsed_json = json.loads(clean_text)
                structured_data = WebAnalyserOutput(**parsed_json)
            except Exception as e:
                structured_data = WebAnalyserOutput(**data["web_analysis"])
               
        except Exception as e:
            print("Error in WebAnalyserTool: ", e)
            structured_data = WebAnalyserOutput(
                article_body=[], topic=[], entities=[]
            )
        return structured_data.model_dump()
