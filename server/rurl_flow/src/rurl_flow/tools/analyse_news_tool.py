from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from crewai import LLM
from dotenv import load_dotenv

_ = load_dotenv()

class AnalyseNewsToolInput(BaseModel):
    """Input schema for AnalyseNewsTool."""
    argument: str = Field(..., description="Description of the argument.")
    # Update with fields returned from the web_parser tool

class AnalyseNewsToolOutput(BaseModel):
    """Output schema for AnalyseNewsTool."""
    domain: str = Field(..., description="Web domain of the article.")
    organisation: str = Field(..., description="Organisation name of the article.")
    author: str = Field(..., description="Author name of the article.")
    title: str = Field(..., description="Title of the article.")
    date: str = Field(..., description="Date of publication of the article.")
    topic: str = Field(..., description="Topic of the article.")
    summary: str = Field(..., description="Content summary of the article.")

class AnalyseNewsTool(BaseTool):
    name: str = "News Analysis Tool"
    description: str = (
        "This tool extracts the web domain, organisation name, author name, title of article, date of publication, the article topic and content summary from a parsed document."
    )
    
    # Update with fields returned from the web_parser tool
    args_schema: Type[BaseModel] = AnalyseNewsToolInput


    class Config:
        arbitrary_types_allowed = True

    def _run(self, argument: str) -> str:
        # Implementation goes here
        llm: LLM = LLM(
            model="openai/gpt-4o",
            temperature=0.2,
            response_format=AnalyseNewsToolOutput
        )
        return llm.call("wow! this is a")

if __name__ == "__main__":
    tool = AnalyseNewsTool()
    data = AnalyseNewsToolInput(argument="this is an example of an argument")
    print(tool.run(data))