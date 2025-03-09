import asyncio
import os
from typing import Type, List, Dict
from pydantic import BaseModel, Field

from tavily import TavilyClient
from crewai.tools import BaseTool

# get the article body from the data
async def web_search(article_body):
      # init tavily client
      tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

      async def run_search(section):
          print(f"Running web search for section: {section['id']}")
          return await asyncio.to_thread(tavily_client.search, f"Fact check: {section['content']}")

      # run web search for each article body item
      tasks = [run_search(section) if section['to_fact_check'] else None for section in article_body]
      search_results = await asyncio.gather(*tasks)

      # append to article body
      for i, section in enumerate(article_body):
          if section['to_fact_check']:
              section['search_results'] = search_results[i]
      
      return search_results

class TavilyToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    article_body: List[Dict] = Field(..., description="Description of the argument.")

class TavilyTool(BaseTool):
    name: str = "Tavily websearch tool"
    description: str = (
        "This tool takes in a list of article bodies and searches the web for contents to fact check against."
    )
    args_schema: Type[BaseModel] = TavilyToolInput

    async def _run(self, article_body: List[Dict]) -> List[Dict]:
      res = await web_search(article_body)
      return res
