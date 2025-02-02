import flet as ft
from modules.config_loader import update_domain_address_in_config, save_ip_to_inventory

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
