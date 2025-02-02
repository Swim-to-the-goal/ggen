import flet as ft
from modules.plan_changes import get_planned_changes
from modules.config_loader import load_config, save_config_to_yaml
from modules.apply_changes import apply_changes
from modules.update_edit_config_tab import create_edit_config_tab 

def show_planned_changes_form(page: ft.Page, selected_services):
    current_config = load_config()
    backup_config = current_config.copy()  
    new_config = {service: {"enabled": True} for service in selected_services}
    changes = get_planned_changes(current_config, new_config)
    show_planned_changes(page, changes, selected_services, backup_config)

def show_planned_changes(page, changes, selected_services, backup_config):
    change_text = "Changes:\n"
    for change_type, services in changes.items():
        if change_type == "remove":
            change_text += "These services were enabled before, but will be removed:\n"
        elif change_type == "disable":
            change_text += "These services will be disabled:\n"
        else:
            change_text += f"{change_type.capitalize()}:\n"
        for service in services:
            change_text += f"  - {service}\n"

    dialog = ft.AlertDialog(
        title=ft.Text("Planned Changes"),
        content=ft.Text(change_text),
        actions=[
            ft.TextButton("Apply", on_click=lambda _: apply_and_confirm(page, changes, selected_services)),
            ft.TextButton("Cancel", on_click=lambda _: cancel_changes(page, dialog, backup_config))
        ]
    )
    page.dialog = dialog
    dialog.open = True
    page.update()

def apply_and_confirm(page, changes, selected_services):
    new_config = {service: {"enabled": True} for service in selected_services}
    applied_changes = apply_changes(new_config)
    page.snack_bar = ft.SnackBar(ft.Text("Changes Applied Successfully!"))
    page.snack_bar.open = True
    page.update()
    close_dialog(page, page.dialog)
    switch_to_edit_config_tab(page, selected_services)

def cancel_changes(page, dialog, backup_config):
    save_config_to_yaml(backup_config) 
    close_dialog(page, dialog)

def close_dialog(page, dialog):
    dialog.open = False
    page.update()

def switch_to_edit_config_tab(page, selected_services):
    for tab in page.controls:
        if isinstance(tab, ft.Tabs):
            tab.selected_index = 2  
            tab.tabs[2].content = ft.Column(create_edit_config_tab(page, selected_services), scroll=ft.ScrollMode.AUTO)
            page.update()
            return
