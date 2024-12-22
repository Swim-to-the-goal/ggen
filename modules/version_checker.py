import json
import subprocess

def get_current_version():
    with open("version.json", "r") as f:
        version_info = json.load(f)
    return version_info["version"]

def get_latest_commit():
    result = subprocess.run(["git", "ls-remote", "https://github.com/Swim-to-the-goal/ggen.git", "refs/heads/main"],
                            stdout=subprocess.PIPE, text=True)
    latest_commit = result.stdout.split("\t")[0]
    return latest_commit.strip()

def is_update_required(current_version, latest_version):
    return current_version != latest_version

def show_update_message(page):
    dialog = ft.AlertDialog(
        title="Update Available",
        content=ft.Text("A new version of the app is available. Please update to the latest version."),
        actions=[
            ft.TextButton("Update", on_click=lambda _: open_update_link(page))
        ]
    )
    page.dialog = dialog
    dialog.open = True
    page.update()

def open_update_link(page):
    ft.open("https://github.com/Swim-to-the-goal/ggen")

def check_for_updates(page):
    current_version = get_current_version()
    latest_commit = get_latest_commit()
    if is_update_required(current_version, latest_commit):
        show_update_message(page)
