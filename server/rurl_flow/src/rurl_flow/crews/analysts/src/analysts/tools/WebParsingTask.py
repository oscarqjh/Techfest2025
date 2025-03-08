from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

from firecrawl import FirecrawlApp

from rurl_flow.src.rurl_flow.tools.globals import firecrawl_app

"""
This is a tool that extracts data from a URL.

Returns:
    weblink: str
    title: str
    content: str
    image_url: list[str]
    date: str
"""

class ExtractSchema(BaseModel): #acts as output schema as well
    """Firecrawl schema for extracting data from a webpage"""
    weblink: str
    title: str
    content: str
    image_url: list[str]
    date: str
class WebParsingTaskInput(BaseModel):
    """Input schema for WebParsingTask"""
    url: str = Field(..., description="URL of the webpage to be parsed")

class WebParsingTask(BaseTool):
    name: str = "WebParsingTool"  # This is the name you reference in tasks.yaml
    description: str = "This tool extracts data from a webpage"
    app: FirecrawlApp = firecrawl_app
    args_schema: Type[BaseModel] = WebParsingTaskInput

    class Config:
        arbitrary_types_allowed = True  # Allow arbitrary types like FirecrawlApp

    def _run(self, url: str) -> dict:
        data = self.app.extract([url], {
            'prompt': 'Extract the date of publish, content from the URL and the images related to the content if available',
            'schema': ExtractSchema.model_json_schema(),
        })
        # Validate and structure the extracted data using ExtractSchema
        structured_data = ExtractSchema(**data["data"])
        return structured_data.model_dump()
