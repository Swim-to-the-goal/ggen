import flet as ft
import os
import yaml

# Create necessary folders
def setup_folders():
    app_folder = "app_data"
    if not os.path.exists(app_folder):
        os.makedirs(app_folder)

# Load configuration from the YAML file
def load_config():
    config_file = "config.yaml"
    if os.path.exists(config_file):
        with open(config_file, "r") as yaml_file:
            return yaml.safe_load(yaml_file)
    else:
        return {}

# Save configuration to the YAML file
def save_config_to_yaml(config_data):
    config_file = "config.yaml"
    with open(config_file, "w") as yaml_file:
        yaml.dump(config_data, yaml_file)

# Save domain configuration to domain.yaml
def save_domain_to_yaml(domain_data):
    domain_file = "domain.yaml"
    with open(domain_file, "w") as yaml_file:
        yaml.dump(domain_data, yaml_file)

# Update the service configuration based on selected services
def update_service_config(selected_services):
    config_data = load_config()
    services = ["mariadb", "mysql", "postgresql", "minio", "redis"]
    for service in services:
        if service in config_data:
            config_data[service]["enabled"] = service in selected_services
    save_config_to_yaml(config_data)

# Create the "Select Services" tab
def create_services_tab(page: ft.Page, selected_services):
    services = ["mariadb", "mysql", "postgresql", "minio", "redis"]
    checkboxes = []

    # Handle checkbox change event
    def on_checkbox_change(service_name, e):
        if e.control.value:
            selected_services.add(service_name)
        else:
            selected_services.discard(service_name)
        page.update()

    # Create checkboxes for each service
    for service in services:
        checkbox = ft.Checkbox(
            label=service.capitalize(),
            value=(service in selected_services),
            on_change=lambda e, service=service: on_checkbox_change(service, e),
        )
        checkboxes.append(checkbox)

    # Create the save button
    save_button = ft.ElevatedButton(
        text="Save Selected Services",
        on_click=lambda e: on_services_save_button_click(page, selected_services)
    )

    return ft.Column([*checkboxes, save_button])

# Handle the save button click event in the "Select Services" tab
def on_services_save_button_click(page, selected_services):
    update_service_config(selected_services)
    update_edit_config_tab(page, selected_services)
    page.add(ft.Text("Configuration saved successfully!", color="green"))
    page.update()

# Create the main input form
def create_input_form(page: ft.Page):
    domain_input = ft.TextField(label="Domain", width=300)
    ip_input = ft.TextField(label="IP", width=300)
    output_label = ft.Text("", color="green")

    # Handle the submit button click event
    def on_submit(e):
        domain = domain_input.value
        ip = ip_input.value
        save_domain_to_yaml({"domain": domain, "ip": ip})
        output_label.value = "Configuration saved to domain.yaml!"
        page.update()

    return ft.Column([
        ft.Text("Main Page", size=30),
        domain_input,
        ip_input,
        ft.ElevatedButton("Save to domain.yaml", on_click=on_submit),
        output_label,
    ])

# Create the "Edit Config" tab
def create_edit_config_tab(page: ft.Page, selected_services):
    config_data = load_config()
    selected_config = {key: config_data[key] for key in selected_services if key in config_data}
    
    controls = []
    for service, config in selected_config.items():
        controls.append(ft.Text(f"{service.capitalize()} Configuration:", size=18, weight="bold"))
        service_controls = []
        for key, value in config.items():
            if key != "enabled":  # Skip the "enabled" field
                service_controls.append(ft.TextField(label=key, value=value, width=200))
        controls.append(ft.Row(service_controls, wrap=True))

    def on_save_changes(e):
        new_config = {}
        for control in controls:
            if isinstance(control, ft.Row):
                for sub_control in control.controls:
                    if isinstance(sub_control, ft.TextField):
                        key, service = sub_control.label, sub_control.data
                        if service not in new_config:
                            new_config[service] = {}
                        new_config[service][key] = sub_control.value
        for key in selected_services:
            if key in new_config:
                config_data[key] = new_config[key]
        save_config_to_yaml(config_data)
        page.add(ft.Text("Configuration saved successfully!", color="green"))
        page.update()

    save_button = ft.ElevatedButton(text="Save Changes", on_click=on_save_changes)
    controls.append(save_button)
    return ft.Column(controls)

# Update the "Edit Config" tab with selected services
def update_edit_config_tab(page, selected_services):
    edit_config_tab = create_edit_config_tab(page, selected_services)
    for tab in page.controls:
        if isinstance(tab, ft.Tabs):
            for t in tab.tabs:
                if t.text == "Edit Config":
                    t.content = edit_config_tab
                    page.update()
                    return

# Create tabs for the application
def create_tabs(page: ft.Page, selected_services):
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="Main", content=create_input_form(page)),
            ft.Tab(text="Select Services", content=create_services_tab(page, selected_services)),
            ft.Tab(text="Edit Config", content=create_edit_config_tab(page, selected_services)),
        ],
    )
    page.add(tabs)

# Main function to run the application
def main(page: ft.Page):
    page.title = "Tab-Based App"
    selected_services = set()
    setup_folders()
    create_tabs(page, selected_services)

ft.app(target=main)
