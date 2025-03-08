from __future__ import annotations
from crewai.tools import BaseTool
from typing import Type, TYPE_CHECKING
from pydantic import BaseModel, Field
from .globals import firecrawl_app
from firecrawl import FirecrawlApp


"""
This is a tool that extracts data from a URL.

Returns:
    weblink: str
    title: str
    content: str
    image_urls: list[str]
    date: str
"""


class ExtractSchema(BaseModel):  # acts as output schema as well
    """Firecrawl schema for extracting data from a webpage"""

    weblink: str
    domain: str
    title: str
    content: str
    image_urls: list[str]
    date: str


class WebParsingToolInput(BaseModel):
    """Input schema for WebParsingTool"""

    url: str = Field(..., description="URL of the webpage to be parsed")


class WebParsingTool(BaseTool):
    name: str = "WebParsing"  # This is the name you reference in tasks.yaml
    description: str = "This tool extracts data from a webpage"
    app: FirecrawlApp = firecrawl_app
    args_schema: Type[BaseModel] = WebParsingToolInput

    class Config:
        arbitrary_types_allowed = True  # Allow arbitrary types like FirecrawlApp

    def _run(self, url: str) -> dict:
        data = self.app.extract(
            [url],
            {
                "prompt": "Extract the domain date of publish, content from the URL (paragraphs may be separated, concat them together) and the images related to the content if available",
                "schema": ExtractSchema.model_json_schema(),
            },
        )
        # Validate and structure the extracted data using ExtractSchema
        structured_data = ExtractSchema(**data["data"])
        return structured_data.model_dump()
