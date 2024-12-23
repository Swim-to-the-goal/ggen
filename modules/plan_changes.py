import json
import os
import yaml

def get_planned_changes(current_config, new_config):
    changes = {"add": [], "remove": [], "update": []}
    for service in new_config:
        if service not in current_config:
            changes["add"].append(service)
        elif new_config[service] != current_config[service]:
            changes["update"].append(service)
    for service in current_config:
        if service not in new_config:
            changes["remove"].append(service)
    return changes

def save_state(state, filename="state.json"):
    with open(filename, "w") as f:
        json.dump(state, f)

def load_state(filename="state.json"):
    if not os.path.exists(filename) or os.stat(filename).st_size == 0:
        return {}  
    with open(filename, "r") as f:
        state = json.load(f)
    return state

def load_config(filename="app_data/config.yaml"):
    if not os.path.exists(filename):
        return {} 
    with open(filename, "r") as f:
        config = yaml.safe_load(f)
    return config
