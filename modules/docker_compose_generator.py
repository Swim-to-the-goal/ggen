import os
from jinja2 import Template
from modules.config_loader import load_config

def generate_docker_compose(template_name, output_name, config_data):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    templates_path = os.path.join(current_dir, "../app_data/templates")
    template_path = os.path.join(templates_path, template_name)
    output_path = output_name

    if os.path.exists(template_path):
        with open(template_path, "r") as file:
            template = Template(file.read())
            rendered = template.render(config_data)

        with open(output_path, "w") as output_file:
            output_file.write(rendered)
        print(f"{output_name} generated successfully!")
    else:
        print(f"Template file {template_name} does not exist.")

def test_generate_docker_compose():
    config_data = load_config()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    templates_path = os.path.join(current_dir, "../app_data/templates")
    templates = [f for f in os.listdir(templates_path) if f.endswith('.j2')]

    if not os.path.exists('infrastructure'):
        os.makedirs('infrastructure')

    for template in templates:
        service_name = template.replace("docker-compose.", "").replace(".j2", "")
        if service_name in config_data and config_data[service_name]["enabled"]:
            output_file = f"infrastructure/docker-compose.{service_name}.yaml"
            generate_docker_compose(template, output_file, {service_name: config_data[service_name]})
        else:
            print(f"Service {service_name} is not defined in config_data or not enabled.")

# اجرای تست
test_generate_docker_compose()
