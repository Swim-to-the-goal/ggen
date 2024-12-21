import flet as ft
import os
import yaml


def setup_folders():
    app_folder = "app_data"
    
    if not os.path.exists(app_folder):
        os.makedirs(app_folder)


def load_config():
    config_file = "config.yaml"  
    
    if os.path.exists(config_file):
        with open(config_file, "r") as yaml_file:
            return yaml.safe_load(yaml_file) 
    else:
        return {}  


def save_config_to_yaml(config_data):
    config_file = "config.yaml"  
    
    with open(config_file, "w") as yaml_file:
        yaml.dump(config_data, yaml_file)


def update_service_config(selected_services):
    config_data = load_config()  


    services = ["mariadb", "mysql", "postgresql", "minio", "redis"]


    for service in services:
        if service in config_data: 
            config_data[service]["enabled"] = service in selected_services  


    save_config_to_yaml(config_data)


def create_services_tab(page: ft.Page, selected_services):

    services = ["mariadb", "mysql", "postgresql", "minio", "redis"]
    checkboxes = []

    def on_checkbox_change(service_name, e):

        if e.control.value:
            selected_services.add(service_name)
        else:
            selected_services.discard(service_name)
        
        page.update() 


    for service in services:
        checkbox = ft.Checkbox(
            label=service.capitalize(),
            value=(service in selected_services),
            on_change=lambda e, service=service: on_checkbox_change(service, e),
        )
        checkboxes.append(checkbox)


    save_button = ft.ElevatedButton(
        text="Save Selected Services", 
        on_click=lambda e: on_services_save_button_click(page, selected_services)
    )

    return ft.Column([*checkboxes, save_button])


def on_services_save_button_click(page, selected_services):
    update_service_config(selected_services)
    page.add(ft.Text("Configuration saved successfully!", color="green"))
    page.update() 


def create_input_form(page: ft.Page):
    domain_input = ft.TextField(label="Domain", width=300)
    ip_input = ft.TextField(label="IP", width=300)
    output_label = ft.Text("", color="green")

    def on_submit(e):
        domain = domain_input.value
        ip = ip_input.value
        save_config_to_yaml({"domain": domain, "ip": ip}) 
        output_label.value = "Configuration saved to all.yaml!"
        page.update()

    return ft.Column([
        ft.Text("Main Page", size=30),
        domain_input,
        ip_input,
        ft.ElevatedButton("Save to all.yaml", on_click=on_submit),
        output_label,
    ])


def create_edit_config_tab(page: ft.Page):

    config_data = load_config()


    config_text = yaml.dump(config_data, allow_unicode=True)


    config_text_field = ft.TextField(
        value=config_text,
        multiline=True, 
        height=400,
        width=500,
        text_style=ft.TextStyle(size=14),
    )


    def on_save_changes(e):
        new_config = yaml.safe_load(config_text_field.value) 
        save_config_to_yaml(new_config) 
        page.add(ft.Text("Configuration saved successfully!", color="green"))
        page.update() 

    save_button = ft.ElevatedButton(text="Save Changes", on_click=on_save_changes)

    return ft.Column([config_text_field, save_button])


def create_tabs(page: ft.Page, selected_services):
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="Main", content=create_input_form(page)),
            ft.Tab(text="Select Services", content=create_services_tab(page, selected_services)),
            ft.Tab(text="Edit Config", content=create_edit_config_tab(page)),
        ],
    )
    page.add(tabs)


def main(page: ft.Page):
    page.title = "Tab-Based App"
    selected_services = set()
    setup_folders()
    create_tabs(page, selected_services) 


ft.app(target=main)
