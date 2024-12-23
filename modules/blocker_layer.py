import flet as ft

def open_update_link(page):
    page.launch_url("https://github.com/Swim-to-the-goal/ggen")

def show_blocker_layer(page):
    blocker = ft.Container(
        content=ft.Column([
            ft.Text("You must update to the latest version to continue using the app.", size=24, weight="bold"),
            ft.ElevatedButton("Update Now", on_click=lambda _: open_update_link(page))
        ]),
        bgcolor="rgba(0, 0, 0, 0.8)", 
        expand=True,
        alignment=ft.alignment.center,
    )
    page.overlay.append(blocker)
    page.update()
