import flet as ft

def create_about_tab(page: ft.Page, version):
    return ft.Column([
        ft.Text("About GGen", size=30, weight="bold", color="black"),
        ft.Divider(),
        ft.Text(f"Version: {version}", size=18, color="blue"),
        ft.Text("Description:", size=20, weight="bold"),
        ft.Text(
            "GGen is designed to streamline the management of your services and configurations. With its user-friendly interface, you can effortlessly customize and deploy services, ensuring a smooth and efficient workflow.",
            size=16,
        ),
        ft.Divider(),
        ft.Text("Contact Information", size=20, weight="bold"),
        ft.Text("Powered by Doech Ltd", size=16),
        ft.Text("Coded and maintained by Ehsan", size=16),
        ft.Text("We can help you to go smoothly :)", size=14, weight="bold"),
        ft.Row([
            ft.Image(src="https://pics.freeicons.io/uploads/icons/png/16983312581574338606-512.png", width=20, height=20),  
            ft.Text(
                "ehsanjahanbakhsh9@gmail.com",
                size=16,
                color="blue",
                selectable=True,  
            ),
        ]),
        ft.Row([
            ft.Image(src="https://pics.freeicons.io/uploads/icons/png/9506131951530100222-512.png", width=20, height=20),  
            ft.Text(
                "linkedin.com/in/ehsan-jahanbakhsh",
                size=16,
                color="blue",
                selectable=True, 
            ),
        ]),
        ft.Divider(),
        ft.Image(src="https://via.placeholder.com/150", width=150, height=150, fit="contain"),
        ft.Text("Thank you for using GGen! We hope it makes your life easier.", size=16, italic=True),
    ], scroll="adaptive")
