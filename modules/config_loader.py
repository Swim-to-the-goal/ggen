import os
import yaml

def load_config():
    config_file = "app_data/config.yaml"
    template_config_file = os.path.join("app_data", "templates", "config.yaml.tmp")

    if not os.path.exists(config_file) and os.path.exists(template_config_file):
        with open(template_config_file, "r") as template_file:
            config_data = yaml.safe_load(template_file)
        with open(config_file, "w") as yaml_file:
            yaml.dump(config_data, yaml_file)
    elif os.path.exists(config_file):
        with open(config_file, "r") as yaml_file:
            config_data = yaml.safe_load(yaml_file)
    else:
        config_data = {}

    for service in config_data.values():
        if isinstance(service, dict) and 'enabled' not in service:
            service['enabled'] = False

    return config_data

def save_config_to_yaml(config_data):
    config_file = "app_data/config.yaml"
    if not os.path.exists("app_data"):
        os.makedirs("app_data")
    with open(config_file, "w") as yaml_file:
        yaml.dump(config_data, yaml_file)

def update_domain_address_in_config(domain):
    config_data = load_config()
    for service in config_data.values():
        if isinstance(service, dict) and 'domain_address' in service:
            service['domain_address'] = domain
    save_config_to_yaml(config_data)

def save_ip_to_inventory(ip):
    inventory_file = "app_data/inventory.yml"
    inventory_data = {"hosts": [{"ip": ip}]}
    with open(inventory_file, "w") as yaml_file:
        yaml.dump(inventory_data, yaml_file)
