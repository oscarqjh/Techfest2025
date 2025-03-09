from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class InsightsTool(BaseModel):
    """Input schema for MyCustomTool."""
    credibility_classification: str = Field(..., description="Credibility of the news site (likely_reliable, unreliable or misinformation).")
    cross_references: str = Field(..., description="Cross references to other news sites.")

class InsightsTool(BaseTool):
    name: str = "Generate a short insight into the credibility of the news site"
    description: str = (
        "This tool receives the credibility classification of a news site and cross references to other news sites to generate a short insight into the credibility of the news site."
    )
    args_schema: Type[BaseModel] = InsightsTool

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."
