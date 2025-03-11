import sys
sys.path.append('/Users/chengyao/Documents/GitHub/Techfest2025/server')

from neondb.apis.credible_api import get_credible_list
from neondb.apis.blacklist_api import get_blacklist
from crewai.tools import BaseTool


class QueryBlacklistTool(BaseTool):
    name: str = "Query Blacklisted Sources Tool"
    description: str = "This tool queries a list of blacklisted, unreliable sources from the internal database."

    def _run(self) -> list[str]:
        blacklisted_sources = ["fake.com"] # Placeholder
        # blacklisted_sources = get_blacklist()
        return blacklisted_sources

class QueryCredibleTool(BaseTool):
    name: str = "Query Credible Sources Tool"
    description: str = "This tool queries a list of credible sources from the internal database."

    def _run(self) -> list[str]:
        credible_sources = ["straitstimes.com"] # Placeholder
        # credible_sources = get_credible_list()
        return credible_sources
