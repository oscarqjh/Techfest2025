import os
from dotenv import load_dotenv
from firecrawl import FirecrawlApp
import openai

load_dotenv()

FIRECRAWL_API = os.getenv("FIRECRAWL_API")
firecrawl_app = FirecrawlApp(api_key=FIRECRAWL_API)

OPENAI_API = os.getenv("OPENAI_API")
client = openai.Client(api_key=OPENAI_API)
# gpt_client = openai.Client(api_key=OPENAI_API)

# GROQ_API = os.getenv("GROQ_API_KEY")
# groq_client = openai.Client(api_key=GROQ_API,
#                     base_url="https://api.groq.com/openai/v1")