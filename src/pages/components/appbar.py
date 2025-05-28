import flet as ft

class MyAppBar(ft.AppBar):
    def __init__(self, page: ft.Page, title: str):
        super().__init__()
        self.page = page
        self.leading = ft.Image(
            src="../../src/assets/new_logo.png",
            width=10,
            height=10,
        )
        self.center_title = True
        self.leading_width = 40
        self.title = ft.Text(title)
        self.actions = [
            ft.IconButton(ft.Icons.ADD),
            ft.IconButton(ft.Icons.REMOVE),
        ]