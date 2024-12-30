import os
import flet as ft
from modules.config_loader import load_config, save_config_to_yaml
from modules.docker_compose_generator import generate_docker_compose

def create_edit_config_tab(page, selected_services):
    config_data = load_config()
    if not selected_services:
        return [ft.Text("No services selected.")]

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
        save_config_to_yaml(new_config)
        page.add(ft.Text("Configuration saved successfully!", color="green"))
        page.update()

    def on_generate_compose_file(e):
        if not os.path.exists('infrastructure'):
            os.makedirs('infrastructure')
        for service in selected_services:
            if service in config_data:
                template_file = f"docker-compose.{service}.j2"
                output_file = f"infrastructure/docker-compose.{service}.yaml"
                service_config = {service: config_data[service]}
                generate_docker_compose(template_file, output_file, service_config)
            else:
                print(f"Service {service} is not defined in config_data")
        page.add(ft.Text("Docker Compose files generated successfully!", color="green"))
        page.update()

    save_button = ft.ElevatedButton(text="Save Changes", on_click=on_save_changes)
    generate_button = ft.ElevatedButton(text="Generate Compose Files", on_click=on_generate_compose_file)

    controls.append(save_button)
    controls.append(generate_button)

    return controls
