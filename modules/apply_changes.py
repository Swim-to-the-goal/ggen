import json
from modules.plan_changes import get_planned_changes, save_state, load_state

def apply_changes(new_config):
    current_config = load_state()
    changes = get_planned_changes(current_config, new_config)

    for service in changes["add"]:
        current_config[service] = new_config[service]
    for service in changes["update"]:
        current_config[service] = new_config[service]
    for service in changes["remove"]:
        del current_config[service]
    
    save_state(current_config)
    return changes
