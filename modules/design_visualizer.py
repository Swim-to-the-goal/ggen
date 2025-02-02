import flet as ft
from modules.config_template_manager import load_design_config_template, get_design_config
import os

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
design_config_template_path = os.path.join(base_path, 'app_data/templates/design-config.yaml.tmp')
img_path = os.path.join(base_path, 'app_data/templates/imgdesign/wordpress_stack.png')

def create_design_image_view(page, design_name, on_back_click, on_next_click):
    design_config_template = load_design_config_template(design_config_template_path)
    design_config = get_design_config(design_name, design_config_template)
    
    design_text = f"Design: {design_name}\n"
    for service, config in design_config.items():
        design_text += f"{service}:\n"
        for key, value in config.items():
            design_text += f"  {key}: {value}\n"
    
    design_label = ft.Text(design_text)
    design_image = ft.Image(src=img_path)
    
    back_button = ft.ElevatedButton(text="Back", on_click=on_back_click)
    next_button = ft.ElevatedButton(text="Next to Config", on_click=on_next_click)
    
    return ft.Column([design_label, design_image, back_button, next_button])
