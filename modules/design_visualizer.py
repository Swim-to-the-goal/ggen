import flet as ft
from modules.config_template_manager import load_design_config_template, get_design_config, save_config_template

def create_design_image_view(page, design_name, on_back_click):
    design_config_template = load_design_config_template('../app_data/templates/design-config.yaml.tmp')
    design_config = get_design_config(design_name, design_config_template)
    
    design_text = f"Design: {design_name}\n"
    for service, config in design_config.items():
        design_text += f"{service}:\n"
        for key, value in config.items():
            design_text += f"  {key}: {value}\n"
    
    design_label = ft.Text(design_text)
    
    back_button = ft.ElevatedButton(text="Back", on_click=on_back_click)
    
    return ft.Column([design_label, back_button])
