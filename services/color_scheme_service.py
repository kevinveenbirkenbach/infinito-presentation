import os
from jinja2 import Environment, FileSystemLoader
from colorscheme_generator import generate_full_palette


class ColorSchemeService:
    def __init__(self, base_color: str, output_path: str):
        self.base_color = base_color
        self.output_path = output_path

    def generate_color_scheme(self):
        # Generate full palette
        palette = generate_full_palette(self.base_color, count=7, shades=100)

        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('css/color.css.j2')

        rendered = template.render(colors=palette.items())

        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(rendered)
