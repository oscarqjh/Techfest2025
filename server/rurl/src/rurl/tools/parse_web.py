from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from .globals import firecrawl_app  

"""
This is a tool that extracts data from a URL.
"""

class ExtractSchema(BaseModel):
    """Firecrawl schema for extracting data from a webpage"""
    weblink: str
    title: str
    content: str
    image_url: list


class web_parsing_task(BaseTool):
    name: str = "web_parser"  # This is the name you reference in tasks.yaml
    app = firecrawl_app

    def _run(self, url: str) -> list:
        data = self.app.extract([url], {
        'prompt': 'Extract the Extract the content from the URL and the images related to the content if available',
        'schema': ExtractSchema.model_json_schema(),
    })
        return data
