from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from serpapi import GoogleSearch
from dotenv import load_dotenv
import os
from urllib.parse import urlparse

_ = load_dotenv()

class ImageWebsearchToolInput(BaseModel):
    """Input schema for SearchSimilarNewsTool."""
    image_url: str = Field(..., description="URL of the image to search for similar news articles.")

class ImageWebsearchToolOutput(BaseModel):
    """Output schema for SearchSimilarNewsTool."""
    articles: list[dict] = Field(..., description="List of similar news articles with title, URL, and image address.")

class ImageWebsearchTool(BaseTool):
    name: str = "News Similarity Search Tool"
    description: str = (
        "This tool takes an image URL as input and returns the top 10 similar news articles using Google Lens (SerpAPI)."
    )
    args_schema: Type[BaseModel] = ImageWebsearchToolInput

    class Config:
        arbitrary_types_allowed = True

    def _run(self, image_url: str) -> dict:
        api_key = os.getenv("SERPAPI_KEY")
        if not api_key:
            return {"error": "SerpAPI key is missing from environment variables."}
        
        params = {
            "engine": "google_lens",
            "url": image_url,
            "api_key": api_key,
        }
        
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            
            if "visual_matches" not in results:
                return {"error": "No visual matches found."}
            
            articles = []
            for match in results["visual_matches"][:10]:  # Get top 10 results
                url = match.get("link", "No URL")
                domain = urlparse(url).netloc if url != "No URL" else "No domain"

                articles.append({
                    "title": match.get("title", "No title"),
                    "url": url,
                    "image": match.get("thumbnail", "No image"),
                    "domain": domain  # Extracted domain
                })
            
            return {"articles": articles}
        except Exception as e:
            return {"error": str(e)}


# # Main function to test the tool
# if __name__ == "__main__":
#     # Example image URL to test
#     image_url = "https://cassette.sphdigital.com.sg/image/straitstimes/68b6b2da8283158ccea61aa84c8cc63482859b78def0655a0fd79a42c1f56af6?w=860"
    
#     # Initialize the ImageWebsearchTool
#     tool = ImageWebsearchTool()
    
#     # Call the tool with the image URL and print the results
#     result = tool._run(image_url)
    
#     # Print the result (either articles or error message)
#     print(result)
