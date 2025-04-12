import os
from utils.markdown_parser import MarkdownParser


class MarketService:
    """
    Service class for loading and parsing market data.

    Usage:
        service = MarketService("/source/docs/market")
        markets = service.load_all_markets()
    """

    def __init__(self, base_path: str):
        self.base_path = base_path

    def _load_market_info(self, market_dir: str) -> dict:
        """
        Load and parse a single market directory.

        Args:
            market_dir (str): Path to the market directory.

        Returns:
            dict: Parsed market information.
        """
        analysis_file = os.path.join(market_dir, "analysis.md")
        diagram_file = os.path.join(market_dir, "diagrams.md")

        market = {
            "id": os.path.basename(market_dir),
            "title": "Unknown Market",
            "introduction": "",
            "analysis_link": "#",
            "diagram1": "",
            "diagram2": "",
            "diagram3": "",
            "beaver": f"{os.path.basename(market_dir).lower().replace(' ', '-')}.png"
        }

        if os.path.exists(analysis_file):
            with open(analysis_file, "r", encoding="utf-8") as f:
                content = f.read()
            market["title"] = MarkdownParser.extract_title(content)
            market["introduction"] = MarkdownParser.extract_section(content, "Introduction")
            market["analysis_link"] = analysis_file

        if os.path.exists(diagram_file):
            with open(diagram_file, "r", encoding="utf-8") as f:
                content = f.read()
            diagrams = MarkdownParser.extract_mermaid_diagrams(content)
            if len(diagrams) >= 1:
                market["diagram1"] = diagrams[0].strip()
            if len(diagrams) >= 2:
                market["diagram2"] = diagrams[1].strip()
            if len(diagrams) >= 3:
                market["diagram3"] = diagrams[2].strip()

        return market

    def load_all_markets(self) -> list:
        """
        Load all markets from the base directory.

        Returns:
            list: Sorted list of markets.
        """
        markets = []
        for item in os.listdir(self.base_path):
            market_dir = os.path.join(self.base_path, item)
            if os.path.isdir(market_dir):
                markets.append(self._load_market_info(market_dir))
        return sorted(markets, key=lambda m: m["title"])
