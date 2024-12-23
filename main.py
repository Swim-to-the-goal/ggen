APP_VERSION = "1.0.1"

import os
import flet as ft
from modules.plan_changes import get_planned_changes, load_state, save_state
from modules.apply_changes import apply_changes
from modules.config_loader import load_config, save_config_to_yaml, update_domain_address_in_config, save_ip_to_inventory
from modules.docker_compose_generator import generate_docker_compose
from modules.prometheus_setup import handle_prometheus_setup
from modules.about import create_about_tab
from modules.version_checker import check_for_updates

def main(page: ft.Page):
    page.title = "GGEN"
    selected_services = set()

    check_for_updates(page, APP_VERSION)

    def create_input_form(page: ft.Page):
        domain_input = ft.TextField(label="Domain", width=300)
        ip_input = ft.TextField(label="IP", width=300)
        output_label = ft.Text("", color="green")

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

    def create_services_tab(page: ft.Page, selected_services):
        services = ["mariadb", "mysql", "postgresql", "minio", "redis", "prometheus"]
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
            text="Show Planned Changes",
            on_click=lambda e: show_planned_changes_form(page, selected_services)
        )

        return ft.Column([*checkboxes, save_button])

    def show_planned_changes_form(page, selected_services):
        current_config = load_config()
        new_config = {service: {"enabled": True} for service in selected_services}
        changes = get_planned_changes(current_config, new_config)
        show_planned_changes(page, changes)

    def show_planned_changes(page, changes):
        change_text = "Changes:\n"
        for change_type, services in changes.items():
            if change_type == "remove":
                change_text += "These services were enabled before, but will be removed:\n"
            else:
                change_text += f"{change_type.capitalize()}:\n"
            for service in services:
                change_text += f"  - {service}\n"
        
        dialog = ft.AlertDialog(
            title=ft.Text("Planned Changes"),
            content=ft.Text(change_text),
            actions=[
                ft.TextButton("Apply", on_click=lambda _: apply_and_confirm(page, changes)),
                ft.TextButton("Cancel", on_click=lambda _: close_dialog(page, dialog))
            ]
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def apply_and_confirm(page, changes):
        new_config = {service: {"enabled": True} for service in selected_services}
        applied_changes = apply_changes(new_config)
        page.snack_bar = ft.SnackBar(ft.Text("Changes Applied Successfully!"))
        page.snack_bar.open = True
        page.update()
        close_dialog(page, page.dialog)

    def close_dialog(page, dialog):
        dialog.open = False
        page.update()

    def create_edit_config_tab(page: ft.Page, selected_services):
        config_data = load_config()
        selected_config = {key: config_data[key] for key in config_data if key in selected_services or (key == "prometheus" and "enabled" in config_data["prometheus"] and config_data["prometheus"]["enabled"])}

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
            for key in config_data:
                if key in new_config:
                    new_config[key]["enabled"] = config_data[key].get("enabled", False)
                else:
                    new_config[key] = config_data[key]
            save_config_to_yaml(new_config)
            page.add(ft.Text("Configuration saved successfully!", color="green"))
            page.update()

        save_button = ft.ElevatedButton(text="Save Changes", on_click=on_save_changes)
        
        def on_generate_docker_compose(e):
            if "prometheus" in selected_services:
                handle_prometheus_setup()
            else:
                generate_docker_compose("docker-compose-mon.j2", "docker-compose-mon.yml")

        generate_button = ft.ElevatedButton(text="Generate Docker Compose", on_click=on_generate_docker_compose)

        controls.append(ft.Row([save_button, generate_button]))
        return ft.Column(controls)

    def update_edit_config_tab(page, selected_services):
        edit_config_tab = create_edit_config_tab(page, selected_services)
        for tab in page.controls:
            if isinstance(tab, ft.Tabs):
                for t in tab.tabs:
                    if t.text == "Edit Config":
                        t.content = edit_config_tab
                        page.update()
                        return

    def create_tabs(page: ft.Page):
        tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(text="Main", content=create_input_form(page)),
                ft.Tab(text="Select Services", content=create_services_tab(page, selected_services)),
                ft.Tab(text="Edit Config", content=create_edit_config_tab(page, selected_services)),
                ft.Tab(text="About", content=create_about_tab(page)),
            ],
        )
        page.add(tabs)

    create_tabs(page)

ft.app(target=main)
