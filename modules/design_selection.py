import os
import flet as ft
from modules.design_visualizer import create_design_image_view
from modules.config_template_manager import load_design_config_template, get_design_config
from modules.config_loader import load_config, save_config_to_yaml  # افزودن توابع لازم

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
design_config_template_path = os.path.join(base_path, 'app_data/templates/design-config.yaml.tmp')

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
        page.add(create_design_image_view(page, design_name, on_back_click, lambda e: show_config_page(page, selected_services)))

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

def show_config_page(page, selected_services):
    config_data = load_config(os.path.join(base_path, 'app_data/config.yaml'))  # بارگذاری کانفیگ
    selected_config = {key: config_data[key] for key in selected_services if key in config_data}

    controls = []
    for service, config in selected_config.items():
        controls.append(ft.Text(f"{service.capitalize()} Configuration:", size=18, weight="bold"))
        service_controls = []
        for key, value in config.items():
            if key != "enabled":
                service_controls.append(ft.TextField(label=key, value=str(value), width=150, height=40, data=service))
        controls.append(ft.Row(service_controls, wrap=True, spacing=10))

    def on_save_changes(e):
        new_config = {}
        for row in controls:
            if isinstance(row, ft.Row):
                for sub_control in row.controls:
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
        save_config_to_yaml(new_config, os.path.join(base_path, 'app_data/config.yaml'))  # ذخیره کانفیگ جدید
        page.add(ft.Text("Configuration saved successfully!", color="green"))
        page.update()

    save_button = ft.ElevatedButton(text="Save Changes", on_click=on_save_changes)
    controls.append(save_button)

    page.controls.clear()
    page.add(ft.Column(controls))
    page.update()
