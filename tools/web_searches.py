from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("tavly_api_key")
if not api_key:
    raise RuntimeError("tavly api does'nt exists check your .env file")

def web_search(query : str):
    tavily_client = TavilyClient(api_key=api_key)
    response = tavily_client.search(query)
    return response

