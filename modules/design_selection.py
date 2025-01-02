import os
import flet as ft
from modules.design_visualizer import create_design_image_view
from modules.config_template_manager import load_design_config_template, get_design_config

base_path = os.path.abspath(os.path.dirname(__file__))
design_config_template_path = os.path.join(base_path, '../app_data/templates/design-config.yaml.tmp')

def create_design_selection(page, selected_services, update_edit_config, on_back_click):
    designs = [
        "LAMP Stack",
        "MEAN Stack",
        "MERN Stack",
        "ELK Stack",
        "WordPress Stack",
    ]

    design_config_template = load_design_config_template(design_config_template_path)

    def on_design_select(e):
        design_name = e.control.value
        design_config = get_design_config(design_name, design_config_template)
        for service, config in design_config.items():
            selected_services.add(service)
        update_edit_config(page, selected_services)
        page.controls.clear()
        page.add(create_design_image_view(page, design_name, on_back_click))


        next_button = ft.ElevatedButton(
            text="Next to Config",
            on_click=lambda e: show_config_page(page, selected_services, design_config)
        )
        page.add(next_button)

    dropdown = ft.Dropdown(
        label="Select Design",
        options=[
            ft.dropdown.Option(text=design) for design in designs
        ],
        on_change=on_design_select,
    )

    back_button = ft.ElevatedButton(
        text="Back",
        on_click=on_back_click
    )

    return ft.Column([dropdown, back_button])

def show_config_page(page, selected_services, design_config):
    config_controls = []
    for service, config in design_config.items():
        config_controls.append(ft.Text(f"{service}: {config}"))

    back_button = ft.ElevatedButton(
        text="Back",
        on_click=lambda e: create_design_selection(page, selected_services, update_edit_config, on_back_click)
    )

    page.controls.clear()
    page.add(ft.Column(config_controls + [back_button]))
    page.update()
