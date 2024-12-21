import flet as ft
import os
import yaml
from jinja2 import Template

# Create necessary folders
def setup_folders():
    app_folder = "app_data"
    if not os.path.exists(app_folder):
        os.makedirs(app_folder)

# Load configuration from the YAML file or template
def load_config():
    config_file = "config.yaml"
    template_config_file = os.path.join("app_data", "templates", "config.yaml.tmp")
    
    if os.path.exists(config_file):
        with open(config_file, "r") as yaml_file:
            return yaml.safe_load(yaml_file)
    elif os.path.exists(template_config_file):
        with open(template_config_file, "r") as yaml_file:
            return yaml.safe_load(yaml_file)
    else:
        return {}

# Save configuration to the YAML file
def save_config_to_yaml(config_data):
    config_file = "config.yaml"
    template_config_file = os.path.join("app_data", "templates", "config.yaml.tmp")
    
    if os.path.exists(template_config_file):
        with open(template_config_file, "r") as yaml_file:
            template_config_data = yaml.safe_load(yaml_file)
        
        for service in config_data:
            if service in template_config_data:
                template_config_data[service].update(config_data[service])
        
        with open(config_file, "w") as yaml_file:
            yaml.dump(template_config_data, yaml_file)
    else:
        with open(config_file, "w") as yaml_file:
            yaml.dump(config_data, yaml_file)

# Update domain_address in config.yaml
def update_domain_address_in_config(domain):
    config_data = load_config()
    for service in config_data.values():
        if isinstance(service, dict) and 'domain_address' in service:
            service['domain_address'] = domain
    save_config_to_yaml(config_data)

# Save IP to inventory.yml
def save_ip_to_inventory(ip):
    inventory_file = "inventory.yml"
    inventory_data = {"hosts": [{"ip": ip}]}
    with open(inventory_file, "w") as yaml_file:
        yaml.dump(inventory_data, yaml_file)

# Update the service configuration based on selected services
def update_service_config(selected_services):
    config_data = load_config()
    services = ["mariadb", "mysql", "postgresql", "minio", "redis", "prometheus"]
    for service in services:
        if service in config_data:
            config_data[service]["enabled"] = service in selected_services
    save_config_to_yaml(config_data)

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

# Main function to run the application
def main(page: ft.Page):
    page.title = "GGen"
    selected_services = set()
    setup_folders()

    # Create the main input form
    def create_input_form(page: ft.Page):
        domain_input = ft.TextField(label="Domain", width=300)
        ip_input = ft.TextField(label="IP", width=300)
        output_label = ft.Text("", color="green")

        # Handle the submit button click event
        def on_submit(e):
            domain = domain_input.value
            ip = ip_input.value
            update_domain_address_in_config(domain)
            save_ip_to_inventory(ip)
            output_label.value = "Configuration saved to inventory.yml and updated in config.yaml!"
            page.update()

        return ft.Column([
            ft.Text("Main Page", size=30),
            domain_input,
            ip_input,
            ft.ElevatedButton("Save Configuration", on_click=on_submit),
            output_label,
        ])

    # Create the "Select Services" tab
    def create_services_tab(page: ft.Page, selected_services):
        services = ["mariadb", "mysql", "postgresql", "minio", "redis", "prometheus"]
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

    # Create the "Edit Config" tab
    def create_edit_config_tab(page: ft.Page, selected_services):
        config_data = load_config()
        selected_config = {key: config_data[key] for key in config_data if key in selected_services or (key == "prometheus" and config_data["prometheus"]["enabled"])}
        
        controls = []
        for service, config in selected_config.items():
            controls.append(ft.Text(f"{service.capitalize()} Configuration:", size=18, weight="bold"))
            service_controls = []
            for key, value in config.items():
                if key != "enabled":
                    service_controls.append(ft.TextField(label=key, value=value, width=200, data=service))
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
        
        # Add the generate button for Docker Compose
        generate_button = ft.ElevatedButton(text="Generate Docker Compose", on_click=lambda e: generate_docker_compose())
        
        controls.append(ft.Row([save_button, generate_button]))
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
                ft.Tab(text="Domain Configuration", content=create_input_form(page)),
                ft.Tab(text="Select Services", content=create_services_tab(page, selected_services)),
                ft.Tab(text="Edit & Generate Config", content=create_edit_config_tab(page, selected_services)),
            ],
        )
        page.add(tabs)

    create_tabs(page, selected_services)

ft.app(target=main)
