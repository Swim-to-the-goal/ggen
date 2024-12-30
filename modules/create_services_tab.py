import flet as ft
from modules.update_edit_config_tab import create_edit_config_tab
from modules.show_planned_changes_form import show_planned_changes_form

def create_services_tab(page: ft.Page, selected_services):
    services = ["mariadb", "mysql", "postgresql", "minio", "redis", "prometheus", "traefik"]
    checkboxes = []

    def on_checkbox_change(service_name, e):
        if e.control.value:
            selected_services.add(service_name)
        else:
            selected_services.discard(service_name)
        create_edit_config_tab(page, selected_services)

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
