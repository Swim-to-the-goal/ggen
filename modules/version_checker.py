import json
import subprocess
import flet as ft
from modules.blocker_layer import show_blocker_layer, open_update_link

def get_current_version():
    return APP_VERSION

def get_latest_version_tags():
    result = subprocess.run(["git", "ls-remote", "--tags", "https://github.com/Swim-to-the-goal/ggen.git"],
                            stdout=subprocess.PIPE, text=True)
    tags = [line.split("/")[-1].strip() for line in result.stdout.split("\n") if line]
    sorted_tags = sorted(tags, key=lambda s: list(map(int, s.split("."))))
    return sorted_tags

def compare_versions(current_version, latest_version):
    current_parts = list(map(int, current_version.split(".")))
    latest_parts = list(map(int, latest_version.split(".")))

    for i in range(len(current_parts)):
        if latest_parts[i] > current_parts[i]:
            return latest_parts[i] - current_parts[i]
    return 0

def show_update_message(page):
    dialog = ft.AlertDialog(
        title=ft.Text("Update Available"),
        content=ft.Text("A new version of the app is available. Please update to the latest version."),
        actions=[
            ft.TextButton("Update", on_click=lambda _: open_update_link(page)),
            ft.TextButton("Remind Me Later", on_click=lambda _: close_dialog(page, dialog))
        ]
    )
    page.dialog = dialog
    dialog.open = True
    page.update()

def close_dialog(page, dialog):
    dialog.open = False
    page.update()

def force_update_message(page):
    show_blocker_layer(page)

def check_for_updates(page, current_version):
    latest_versions = get_latest_version_tags()

    if not latest_versions:
        print("Error: No tags found in the repository.")
        return

    latest_version = latest_versions[-1]
    print("Current version:", current_version)
    print("Latest version:", latest_version)
    version_difference = compare_versions(current_version, latest_version)

    if version_difference == 1:
        show_update_message(page)
    elif version_difference >= 2:
        force_update_message(page)
