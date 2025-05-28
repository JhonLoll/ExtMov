import flet as ft

class Home(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(
             controls=[
                    ft.Text("Home"),
                    ft.ElevatedButton("Upload", on_click=self.upload_file),
                ],
        )
        self.page = page

    def upload_file(self, e):
            self.page.go("/upload")

