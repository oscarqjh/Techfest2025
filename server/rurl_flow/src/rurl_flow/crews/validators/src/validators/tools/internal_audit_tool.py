from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from crewai import LLM
from dotenv import load_dotenv

_ = load_dotenv()

class InternalAuditToolInput(BaseModel):
    """Input schema for InternalAuditTool."""
    domain: str = Field(..., description="Web domain of the article.")
    # author: str = Field(..., description="Author name of the article.")
    blacklisted_sources: list[str] = Field(..., description="List of blacklisted sources.")
    credible_sources: list[str] = Field(..., description="List of credible sources.")

class InternalAuditToolOutput(BaseModel):
    """Output schema for InternalAuditTool."""
    is_blacklisted: bool = Field(..., description="Whether the source is blacklisted or not.")
    is_credible: bool = Field(..., description="Whether the source is credible or not.")

class InternalAuditTool(BaseTool):
    name: str = "Internal Audit Tool"
    description: str = "This tool compares the website domain and author name of an article with the internal database of blacklisted unreliable sources and credible sources."
    
    # Update with fields returned from the web_parser tool
    args_schema: Type[BaseModel] = InternalAuditToolInput

    def _run(self, domain: str, blacklisted_sources: list[str], credible_sources: list[str]) -> str:
        # Check if domain is in blacklisted_sources
        if domain in blacklisted_sources:
            is_blacklisted = True
        else:
            is_blacklisted = False
        # Check if domain is in cerdible_sources
        if domain in credible_sources:
            is_credible = True
        else:
            is_credible = False
        return is_blacklisted, is_credible

if __name__ == "__main__":
    tool = InternalAuditTool()
    data = InternalAuditToolInput(domain="straitstimes.com", blacklisted_sources=["fake.com"], credible_sources=["straitstimes.com"])
    print(tool.run(data))