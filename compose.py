import os
import yaml
from jinja2 import Template

# Load configuration from the YAML file
def load_config():
    config_file = "config.yaml"
    if os.path.exists(config_file):
        with open(config_file, "r") as yaml_file:
            return yaml.safe_load(yaml_file)
    else:
        return {}

# Generate docker-compose files using Jinja2 templates
def generate_docker_compose():
    config_data = load_config()
    templates_path = "app_data/templates"
    output_folder = "."

    for template_file in os.listdir(templates_path):
        if template_file.endswith(".j2"):
            template_path = os.path.join(templates_path, template_file)
            output_file_name = os.path.splitext(template_file)[0] + ".yml"
            output_path = os.path.join(output_folder, output_file_name)

            with open(template_path, "r") as file:
                template = Template(file.read())
                rendered = template.render(config_data)

            with open(output_path, "w") as output_file:
                output_file.write(rendered)
            print(f"{output_file_name} generated successfully!")

# Main function to run the script
def main():
    generate_docker_compose()

if __name__ == "__main__":
    main()
