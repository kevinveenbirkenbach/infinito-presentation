import os
from flask import Flask, render_template

# Initialize the CacheManager
cache_manager = CacheManager()

# Clear cache on startup
cache_manager.clear_cache()

# Hole die Umgebungsvariable FLASK_ENV oder setze einen Standardwert
FLASK_ENV = os.getenv("FLASK_ENV", "production")
    
@app.route('/')
def index():
    return render_template("index.html.j2", cards=app.config["cards"], company=app.config["company"], navigation=app.config["navigation"], platform=app.config["platform"])

if __name__ == "__main__":
    app.run(debug=(FLASK_ENV == "development"), host="0.0.0.0", port=5000)
