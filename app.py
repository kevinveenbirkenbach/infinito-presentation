import os
from flask import Flask, render_template
from services.market_service import MarketService
from services.role_service import RoleService
from services.app_url_service import AppUrlService
from services.docs_link_service import DocsLinkService
from services.template_service import TemplateService
from services.slide_service import SlideService
from utils.background_helper import get_background
from utils.headline_extractor import extract_first_headline
from services.color_scheme_service import ColorSchemeService

app = Flask(__name__)

# Configuration paths
CONFIG_PATH = "config.yml"
MARKETS_PATH = "/source/docs/analysis/market"
ROLES_PATH = "/source/roles"

# Initialize Services
market_service = MarketService(MARKETS_PATH)
role_service = RoleService(ROLES_PATH)
app_url_service = AppUrlService(CONFIG_PATH)
docs_link_service = DocsLinkService(CONFIG_PATH)
template_service = TemplateService(app.template_folder)
slide_service = SlideService()
color_scheme_service = ColorSchemeService(
    base_color=app_url_service.get("base_color"),
    output_path="static/css/color.css"
)
color_scheme_service.generate_color_scheme()

@app.template_global()
def background(file_path):
    return get_background(app.template_folder, file_path)

@app.context_processor
def inject_markets():
    """Inject markets into all templates."""
    return dict(markets=market_service.load_all_markets())

@app.template_global()
def headlines(subdir):
    return [
        {"id": section_id, "headline": headline}
        for file in template_service.list_snippets(subdir)
        for section_id, headline in [extract_first_headline(os.path.join(app.template_folder, file))]
        if headline
    ]

@app.template_global()
def app_url(application_id):
    """Generate application URL."""
    return app_url_service.generate_url(application_id)


@app.template_global()
def docs_link(source_path):
    """Generate documentation link."""
    return docs_link_service.generate_link(source_path)


@app.template_global()
def roles(prefix=None, required_tags=None):
    """Return roles filtered by prefix and tags."""
    return role_service.list_roles_with_meta(prefix=prefix, required_tags=required_tags)


@app.template_global()
def snippets(subdir):
    """Return list of snippet files for a given subdirectory."""
    return template_service.list_snippets(subdir)


@app.before_request
def register_slide_extractor():
    """Register extract_slide globally in Jinja2 environment."""
    app.jinja_env.globals['extract_slide'] = slide_service.extract_content


@app.route('/')
def index():
    """Render the main presentation page."""
    return render_template('index.html.j2')

if __name__ == "__main__":
    # Read host, port and debug from environment (with sensible defaults)
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() in ("1", "true", "yes")

    app.run(host=host, port=port, debug=debug)