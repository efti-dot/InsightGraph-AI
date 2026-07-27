import os
from langchain_tavily import TavilySearch
from app.config import settings

os.environ.setdefault("TAVILY_API_KEY", settings.tavily_api_key)


def search_web(query: str, max_results: int = 5) -> list[dict]:
    tool = TavilySearch(max_results=max_results, topic="general")
    response = tool.invoke({"query": query})
    return response.get("results", [])