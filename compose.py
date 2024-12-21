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

# Generate docker-compose.yml using Jinja2 template
def generate_docker_compose():
    config_data = load_config()
    template_path = os.path.join("app_data", "templates", "docker-compose.j2")
    output_path = "docker-compose.yml"

    if os.path.exists(template_path):
        with open(template_path, "r") as template_file:
            template = Template(template_file.read())
            rendered = template.render(config_data)
            with open(output_path, "w") as output_file:
                output_file.write(rendered)
        print("docker-compose.yml generated successfully!")
    else:
        print(f"Template file {template_path} not found.")

# Main function to run the script
def main():
    generate_docker_compose()

if __name__ == "__main__":
    main()
