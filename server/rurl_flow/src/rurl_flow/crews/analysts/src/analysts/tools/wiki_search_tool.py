from __future__ import annotations
from crewai.tools import BaseTool
from typing import Type, List, TYPE_CHECKING
from pydantic import BaseModel, Field
from .globals import firecrawl_app
from firecrawl import FirecrawlApp
from llm_client import llm_client

"""
This is a tool that performs a wiki search with a list of entities and returns the wiki URL and summary.

Returns:
    list[dict]: List of dictionaries containing the wiki URL and Summary
        wiki_url: str
        summary: str
"""


class WikiSearchSchema(BaseModel):
    """Schema for wiki search results"""

    entity: str
    wiki_url: str
    summary: str
    infobox: str


class WikiSearchToolInput(BaseModel):
    """Input schema for WikiSearchTool"""

    entities: List[str] = Field(
        ..., description="List of entities to search on Wikipedia"
    )


class WikiSearchTool(BaseTool):
    name: str = "WikiSearch"  # This is the name you reference in tasks.yaml
    description: str = "This tool performs a wiki search with a list of entities and returns the wiki URL and summary"
    app: FirecrawlApp = firecrawl_app
    args_schema: Type[BaseModel] = WikiSearchToolInput

    class Config:
        arbitrary_types_allowed = True  # Allow arbitrary types like FirecrawlApp

    def _run(self, entities: List[str]) -> dict:
        results = []
        final_results = []
        for entity in entities:
            wiki_data = self.app.extract(
                ["www.wikipedia.org"],
                {
                    "prompt": f"Search Wikipedia for the entity '{entity}' and return the wiki URL, summary section and infobox information that includes personal details",
                    "schema": WikiSearchSchema.model_json_schema(),
                },
            )
            # Validate and structure the extracted data using WikiSearchSchema
            wiki_data_structured = WikiSearchSchema(**wiki_data["wiki_analysis"])
            results.append(wiki_data)

        # call llm
        for result in results:
            data = llm_client.call_openai_api(result, "WikiSearch")
            final_results.append(data)

        return final_results
