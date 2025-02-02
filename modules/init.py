# APP_VERSION = "1.0.1"

# import os
# import flet as ft
# import subprocess
# from modules.plan_changes import load_state, save_state
# from modules.apply_changes import apply_changes
# from modules.config_loader import load_config, save_config_to_yaml, update_domain_address_in_config, save_ip_to_inventory
# from modules.docker_compose_generator import generate_docker_compose
# from modules.prometheus_setup import handle_prometheus_setup
# from modules.about import create_about_tab
# from modules.version_checker import check_for_updates
# from modules.create_input_form import create_input_form
# from modules.create_services_tab import create_services_tab, create_services_selection, create_design_selection
# from modules.show_planned_changes_form import show_planned_changes_form
# from modules.update_edit_config_tab import create_edit_config_tab
# from modules.design_visualizer import create_design_image_view
# from modules.config_template_manager import load_config_template, save_config_template, load_design_config_template


# try:
#     subprocess.run(["python", "modules/init.py"], check=True)
# except subprocess.CalledProcessError as e:
#     print(f"Initialization script failed: {e}")
#     print("Continuing with the project...")

# def main(page: ft.Page):
#     page.title = "GGEN"
#     selected_services = set()


#     config_template = load_config_template('app_data/templates/config.yaml.tmp')
#     design_config_template = load_design_config_template('app_data/templates/design-config.yaml.tmp')


#     save_config_template(config_template, 'app_data/config.yaml')
#     save_config_template(design_config_template, 'app_data/design-config.yaml')

#     page.theme = ft.Theme(
#         scrollbar_theme=ft.ScrollbarTheme(
#             track_color={
#                 ft.MaterialState.HOVERED: ft.Colors.AMBER,
#                 ft.MaterialState.DEFAULT: ft.Colors.TRANSPARENT,
#             },
#             track_visibility=True,
#             track_border_color=ft.Colors.BLUE,
#             thumb_visibility=True,
#             thumb_color={
#                 ft.MaterialState.HOVERED: ft.Colors.RED,
#                 ft.MaterialState.DEFAULT: ft.Colors.GREY_300,
#             },
#             thickness=30,
#             radius=15,
#             main_axis_margin=5,
#             cross_axis_margin=10,
#         )
#     )

#     check_for_updates(page, APP_VERSION)

#     def on_checkbox_change(service_name, e):
#         if e.control.value:
#             selected_services.add(service_name)
#         else:
#             selected_services.discard(service_name)
#         update_edit_config(page, selected_services)

#     def on_select_change(e):
#         if e.control.value == "Select Services":
#             page.controls.clear()
#             page.add(create_services_selection(page, selected_services, on_checkbox_change, show_planned_changes_form, on_back_click))
#         elif e.control.value == "Select Design":
#             page.controls.clear()
#             page.add(create_design_selection(page, selected_services, update_edit_config, on_back_click))

#     def on_back_click(e):
#         page.controls.clear()
#         create_tabs(page)

#     def on_view_design(e):
#         design_name = e.control.value
#         page.controls.clear()
#         page.add(create_design_image_view(page, design_name, on_back_click))

#     def update_edit_config(page, selected_services):

#         config_data = load_config()
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#         templates_path = os.path.join(current_dir, "app_data/templates")
#         templates = [f for f in os.listdir(templates_path) if f.endswith('.j2')]

#         if not os.path.exists('infrastructure'):
#             os.makedirs('infrastructure')

#         for template in templates:
#             service_name = template.replace("docker-compose.", "").replace(".j2", "")
#             if service_name in config_data and config_data[service_name]["enabled"]:
#                 output_file = f"infrastructure/docker-compose.{service_name}.yaml"
#                 generate_docker_compose(template, output_file, {service_name: config_data[service_name]})
#             else:
#                 print(f"Service {service_name} is not defined in config_data or not enabled.")

#         edit_config_controls = create_edit_config_tab(page, selected_services)
#         for tab in page.controls:
#             if isinstance(tab, ft.Tabs):
#                 for t in tab.tabs:
#                     if t.text == "Edit Config":
#                         t.content.controls.clear()
#                         t.content.controls.extend(edit_config_controls)
#                         page.update()
#                         return

#     def create_tabs(page: ft.Page):
#         tabs = ft.Tabs(
#             selected_index=0,
#             tabs=[
#                 ft.Tab(text="Main", content=create_input_form(page)),
#                 ft.Tab(text="Select Services", content=create_services_tab(page, selected_services, on_checkbox_change, show_planned_changes_form, on_select_change)),
#                 ft.Tab(text="Edit Config", content=ft.Column(create_edit_config_tab(page, selected_services), scroll=ft.ScrollMode.AUTO)),
#                 ft.Tab(text="About", content=create_about_tab(page, APP_VERSION)),
#             ],
#         )
#         page.add(tabs)

#     create_tabs(page)

# ft.app(target=main)
