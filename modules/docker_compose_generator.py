import os
import yaml
from jinja2 import Template
from modules.config_loader import load_config

def generate_docker_compose(template_name, output_name):
    config_data = load_config()
    templates_path = "app_data/templates"
    template_path = os.path.join(templates_path, template_name)
    output_path = output_name

    if os.path.exists(template_path):
        with open(template_path, "r") as file:
            template = Template(file.read())
            rendered = template.render(config_data)

        with open(output_path, "w") as output_file:
            output_file.write(rendered)
        print(f"{output_name} generated successfully!")
