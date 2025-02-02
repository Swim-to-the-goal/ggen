import yaml

def load_config_template(template_path):
    print(f"Loading config template from: {template_path}")
    with open(template_path, 'r') as file:
        return yaml.safe_load(file)

def save_config_template(config, template_path):
    with open(template_path, 'w') as file:
        yaml.safe_dump(config, file)

def load_design_config_template(template_path):
    print(f"Loading design config template from: {template_path}")
    with open(template_path, 'r') as file:
        return yaml.safe_load(file)

def get_design_config(design_name, design_config_template):
    return design_config_template.get(design_name, {})
