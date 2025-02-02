import os

APP_VERSION = "1.0.1"

import flet as ft
import subprocess
from modules.plan_changes import load_state, save_state, get_planned_changes
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
from modules.config_template_manager import load_config_template, save_config_template, load_design_config_template
from modules.design_selection import create_design_selection

# Set the paths as relative
base_path = os.path.abspath(os.path.dirname(__file__))
config_template_path = os.path.join(base_path, 'app_data/templates/config.yaml.tmp')
design_config_template_path = os.path.join(base_path, 'app_data/templates/design-config.yaml.tmp')

print(f"Config Template Path: {config_template_path}")
print(f"Design Config Template Path: {design_config_template_path}")

# Run the init.py script to check and install dependencies only once
try:
    subprocess.run(["python", os.path.join(base_path, "modules/init.py")], check=True)
except subprocess.CalledProcessError as e:
    print(f"Initialization script failed: {e}")
    print("Continuing with the project...")

def main(page: ft.Page):
    page.title = "GGEN"
    selected_services = set()

    if not os.path.exists(config_template_path):
        print(f"File {config_template_path} does not exist.")
    if not os.path.exists(design_config_template_path):
        print(f"File {design_config_template_path} does not exist.")

    # Load the config files
    config_template = load_config_template(config_template_path)
    design_config_template = load_design_config_template(design_config_template_path)

    # Save the config files for use in the project
    save_config_template(config_template, os.path.join(base_path, 'app_data/config.yaml'))
    save_config_template(design_config_template, os.path.join(base_path, 'app_data/design-config.yaml'))

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
        update_config_file(page, selected_services)

    def update_config_file(page, selected_services):
        nonlocal config_template
        for service in config_template:
            config_template[service]["enabled"] = service in selected_services
        save_config_template(config_template, os.path.join(base_path, 'app_data/config.yaml'))

    def on_back_click(e):
        page.controls.clear()
        create_tabs(page)

    def create_tabs(page: ft.Page):
        tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(text="Main", content=create_input_form(page)),
                ft.Tab(text="Select Services Mode", content=create_services_tab(page, selected_services, on_checkbox_change)),
                ft.Tab(text="Select Services Edit Config", content=ft.Column(create_edit_config_tab(page, selected_services), scroll=ft.ScrollMode.AUTO)),
                ft.Tab(text="Design Mode", content=create_design_selection(page, selected_services, update_config_file, on_back_click)),
                ft.Tab(text="About", content=create_about_tab(page, APP_VERSION)),
            ],
        )
        page.add(tabs)

    create_tabs(page)

ft.app(target=main)
