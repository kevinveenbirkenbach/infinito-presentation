import os
import re
import logging

# Set up logging for debugging purposes
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

def extract_title(markdown_content):
    """
    Extracts the title from the markdown content.
    Assumes the title is the first line starting with '#' (e.g., "# Global Market Analysis")
    """
    match = re.search(r"^#\s+(.*)$", markdown_content, re.MULTILINE)
    if match:
        title = match.group(1).strip()
        logging.debug(f"Extracted title: {title}")
        return title
    logging.debug("No title found in the markdown content.")
    return "Unknown Market"

def extract_introduction(markdown_content):
    """
    Extracts the 'Introduction' section from the markdown content.
    Searches for a section titled 'Introduction' (e.g., '## 1. Introduction' or '## Introduction')
    and returns the content until the next heading.
    """
    intro_match = re.search(
        r"(?:##\s+(?:1\.\s+)?Introduction)(.*?)(?:\n##|\Z)",
        markdown_content, re.DOTALL | re.IGNORECASE
    )
    if intro_match:
        introduction = intro_match.group(1).strip()
        logging.debug("Introduction section extracted successfully.")
        return introduction
    logging.debug("Introduction section not found in the markdown content.")
    return ""

def extract_diagrams(diagram_content):
    """
    Extracts diagram code blocks from the diagram markdown content.
    Expects code blocks starting with ```mermaid.
    Returns a dictionary with keys 'diagram1', 'diagram2', and 'diagram3'.
    """
    diagrams = re.findall(r"```mermaid(.*?)```", diagram_content, re.DOTALL)
    result = {}
    if len(diagrams) >= 1:
        result["diagram1"] = diagrams[0].strip()
        logging.debug("Diagram 1 extracted successfully.")
    if len(diagrams) >= 2:
        result["diagram2"] = diagrams[1].strip()
        logging.debug("Diagram 2 extracted successfully.")
    if len(diagrams) >= 3:
        result["diagram3"] = diagrams[2].strip()
        logging.debug("Diagram 3 extracted successfully.")
    if not result:
        logging.debug("No diagrams found in the diagram content.")
    return result

def load_market_info(market_dir):
    """
    For a given market directory, load the information from the analysis and diagram files.
    
    Expects:
      - An 'analyses.md' file (contains the title and introduction).
      - A 'diagrams.md' file (contains the diagrams).
    
    Returns a dictionary with:
      - title: The market title (from the first heading)
      - introduction: The introduction section
      - analysis_link: A link (path) to the markdown analysis file
      - diagram1, diagram2, diagram3: The three diagrams (as text, e.g., Mermaid code)
      - beaver: The filename of the corresponding beaver image (generated from the title)
      - id: A unique id (for example, the directory name)
    """
    logging.debug(f"Loading market info from directory: {market_dir}")

    # Determine the analysis file path
    analysis_path = os.path.join(market_dir, "analyses.md")
    if not os.path.exists(analysis_path):
        # Alternatively, search for a file starting with "analyses."
        analysis_candidates = [f for f in os.listdir(market_dir) if f.startswith("analyses.")]
        if analysis_candidates:
            analysis_path = os.path.join(market_dir, analysis_candidates[0])
            logging.debug(f"Found alternative analysis file: {analysis_path}")
        else:
            analysis_path = None
            logging.debug("No analysis file found in the directory.")

    # Determine the diagram file path (preferably .md)
    diagram_path = os.path.join(market_dir, "diagrams.md")
    if not os.path.exists(diagram_path):
        diagram_path = None
        logging.debug("No diagram file found in the directory.")

    market = {}
    if analysis_path and os.path.exists(analysis_path):
        logging.debug(f"Reading analysis file: {analysis_path}")
        with open(analysis_path, "r", encoding="utf-8") as f:
            analysis_content = f.read()
        market["title"] = extract_title(analysis_content)
        market["introduction"] = extract_introduction(analysis_content)
        market["analysis_link"] = analysis_path  # Can be used as a link to the markdown file
    else:
        market["title"] = "Unknown Market"
        market["introduction"] = ""
        market["analysis_link"] = "#"
        logging.debug("Using default values for market title and introduction.")

    if diagram_path and os.path.exists(diagram_path):
        logging.debug(f"Reading diagram file: {diagram_path}")
        with open(diagram_path, "r", encoding="utf-8") as f:
            diagram_content = f.read()
        diagrams = extract_diagrams(diagram_content)
        market["diagram1"] = diagrams.get("diagram1", "")
        market["diagram2"] = diagrams.get("diagram2", "")
        market["diagram3"] = diagrams.get("diagram3", "")
    else:
        market["diagram1"] = ""
        market["diagram2"] = ""
        market["diagram3"] = ""
        logging.debug("No diagram content loaded, setting diagrams to empty strings.")

    # Set a unique ID (for example, the directory name)
    market["id"] = os.path.basename(market_dir)

    # Generate the beaver image name from the title, for example "Global Market Analysis" -> "global-market-analysis.png"
    beaver_image = market["id"].lower().replace(" ", "-")
    market["beaver"] = beaver_image + ".png"    
    logging.debug(f"Generated beaver image file: {market['beaver']}")

    logging.debug(f"Assigned market ID: {market['id']}")
    return market

def load_all_markets(base_dir):
    """
    Iterates over all subdirectories in 'base_dir' (for example, ../cymais/docs/market)
    and loads the market information for each market.
    
    Returns a sorted list (e.g., sorted by title) of markets.
    """
    logging.debug(f"Loading all markets from base directory: {base_dir}")
    markets = []
    for item in os.listdir(base_dir):
        market_path = os.path.join(base_dir, item)
        market = load_market_info(market_path)
        markets.append(market)
        logging.debug(f"Loaded market: {market['title']}")
    markets.sort(key=lambda m: m["title"])
    logging.debug(f"Total markets loaded: {len(markets)}")
    return markets
