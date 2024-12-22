import flet as ft

def create_about_tab(page: ft.Page):
    return ft.Column([
        ft.Text("About GGen", size=30, weight="bold", color="black"),
        ft.Divider(),
        ft.Text("Welcome to GGen!", size=24, color="darkblue"),
        ft.Text("Version: 1.0.0", size=18, color="blue"),
        ft.Text("Description:", size=20, weight="bold"),
        ft.Text(
            "GGen helps you manage services and configurations efficiently with ease. Our intuitive interface allows you to customize and deploy your services quickly and seamlessly.",
            size=16,
        ),
        ft.Divider(),
        ft.Text("Contact Information", size=20, weight="bold"),
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
