import os
from utils.markdown_parser import MarkdownParser


class MarketService:
    """
    Service class for loading and parsing market data.
    """

    def __init__(self, base_path: str):
        self.base_path = base_path

    def _load_market_info(self, market_dir: str) -> dict:
        """
        Load and parse a single market directory.
        """
        analysis_file = os.path.join(market_dir, "analysis.md")
        diagram_file = os.path.join(market_dir, "diagrams.md")

        if not os.path.exists(analysis_file):
            raise FileNotFoundError(f"Missing analysis.md in {market_dir}")

        if not os.path.exists(diagram_file):
            raise FileNotFoundError(f"Missing diagrams.md in {market_dir}")

        with open(analysis_file, "r", encoding="utf-8") as f:
            content = f.read()

        title = MarkdownParser.extract_title(content)
        if not title or title == "Unknown":
            raise ValueError(f"Missing or invalid title in {analysis_file}")

        introduction = MarkdownParser.extract_section(content, "1. Introduction")
        if not introduction:
            raise ValueError(f"Missing 'Introduction' section in {analysis_file}")

        with open(diagram_file, "r", encoding="utf-8") as f:
            content = f.read()

        diagrams = MarkdownParser.extract_mermaid_diagrams(content)
        if not diagrams:
            raise ValueError(f"No Mermaid diagrams found in {diagram_file}")

        return {
            "id": os.path.basename(market_dir),
            "title": title,
            "introduction": introduction,
            "analysis_link": analysis_file,
            "diagram1": diagrams[0].strip(),
            "diagram2": diagrams[1].strip() if len(diagrams) >= 2 else "",
            "diagram3": diagrams[2].strip() if len(diagrams) >= 3 else "",
            "beaver": f"{os.path.basename(market_dir).lower().replace(' ', '-')}.png"
        }

    def load_all_markets(self) -> list:
        """
        Load all markets from the base directory.
        """
        if not os.path.exists(self.base_path):
            raise FileNotFoundError(f"Market path not found: {self.base_path}")

        markets = []
        for item in os.listdir(self.base_path):
            market_dir = os.path.join(self.base_path, item)
            if os.path.isdir(market_dir):
                markets.append(self._load_market_info(market_dir))

        return sorted(markets, key=lambda m: m["title"])