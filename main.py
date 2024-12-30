APP_VERSION = "1.0.1"

import os
import flet as ft
import subprocess
from modules.plan_changes import load_state, save_state
from modules.apply_changes import apply_changes
from modules.config_loader import load_config, save_config_to_yaml, update_domain_address_in_config, save_ip_to_inventory
from modules.docker_compose_generator import generate_docker_compose
from modules.prometheus_setup import handle_prometheus_setup
from modules.about import create_about_tab
from modules.version_checker import check_for_updates
from modules.create_input_form import create_input_form
from modules.create_services_tab import create_services_tab
from modules.show_planned_changes_form import show_planned_changes_form
from modules.update_edit_config_tab import create_edit_config_tab

try:
    subprocess.run(["python", "modules/init.py"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Initialization script failed: {e}")
    print("Continuing with the project...")

def main(page: ft.Page):
    page.title = "GGEN"
    selected_services = set()


    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            track_color={
                ft.MaterialState.HOVERED: ft.Colors.AMBER,
                ft.MaterialState.DEFAULT: ft.Colors.TRANSPARENT,
            },
            track_visibility=True,
            track_border_color=ft.Colors.BLUE,
            thumb_visibility=True,
            thumb_color={
                ft.MaterialState.HOVERED: ft.Colors.RED,
                ft.MaterialState.DEFAULT: ft.Colors.GREY_300,
            },
            thickness=30,
            radius=15,
            main_axis_margin=5,
            cross_axis_margin=10,
        )
    )

    check_for_updates(page, APP_VERSION)

    def on_checkbox_change(service_name, e):
        if e.control.value:
            selected_services.add(service_name)
        else:
            selected_services.discard(service_name)
        update_edit_config(page, selected_services)

    def create_services_tab(page: ft.Page):
        services = ["mariadb", "mysql", "postgresql", "minio", "redis", "prometheus", "traefik"]
        checkboxes = []

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

    def update_edit_config(page, selected_services):
        edit_config_controls = create_edit_config_tab(page, selected_services)
        for tab in page.controls:
            if isinstance(tab, ft.Tabs):
                for t in tab.tabs:
                    if t.text == "Edit Config":
                        t.content.controls.clear()
                        t.content.controls.extend(edit_config_controls)
                        page.update()
                        return

    def create_tabs(page: ft.Page):
        tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(text="Main", content=create_input_form(page)),
                ft.Tab(text="Select Services", content=create_services_tab(page)),
                ft.Tab(text="Edit Config", content=ft.Column(create_edit_config_tab(page, selected_services), scroll=ft.ScrollMode.AUTO)),
                ft.Tab(text="About", content=create_about_tab(page, APP_VERSION)),
            ],
        )
        page.add(tabs)

    create_tabs(page)

ft.app(target=main)
