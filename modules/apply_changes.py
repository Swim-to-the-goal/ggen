from modules.config_loader import load_config, save_config_to_yaml
from modules.plan_changes import get_planned_changes

def apply_changes(new_config):
    current_config = load_config()
    changes = get_planned_changes(current_config, new_config)
    
    if "add" not in changes:
        changes["add"] = []
    if "remove" not in changes:
        changes["remove"] = []
    if "disable" not in changes:
        changes["disable"] = []

    for service in changes["add"]:
        current_config[service] = new_config[service]

    for service in changes["remove"]:
        if service in current_config:
            del current_config[service]

    for service in changes["disable"]:
        if service in current_config:
            current_config[service]["enabled"] = False

    save_config_to_yaml(current_config)
    return changes
