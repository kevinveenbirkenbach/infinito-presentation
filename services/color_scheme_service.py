import os
from jinja2 import Environment, FileSystemLoader
from colorscheme_generator import adjust_color

class ColorSchemeService:
    def __init__(self, base_color: str, output_path: str):
        self.base_color = base_color
        self.output_path = output_path

    def generate_color_scheme(self):
        colors = [
            adjust_color(self.base_color, target_lightness=i / 100)
            for i in range(1, 99)
        ]

        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('css/color.css.j2')

        rendered = template.render(colors=list(enumerate(colors)))

        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(rendered)
