import flet as ft
from pages.components.appbar import MyAppBar
from pages.home import Home
from pages.upload_file import UploadFile

class Routing:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop
        
        self.page.views.append(
            ft.View(
                "/",
                [
                    MyAppBar(self.page, "Home"),
                    Home(self.page),
                ]
            )
        )
        page.update()

    def route_change(self, route):
        print("Route change:", route)
        self.page.views.clear()

        if self.page.route == "/":
            self.page.views.append(
                ft.View(
                    "/",
                    [
                        MyAppBar(self.page, "Home"),
                        Home(self.page),
                    ],
                )
            )
        elif self.page.route == "/upload":
            self.page.views.append(
                ft.View(
                    "/upload",
                    [
                        MyAppBar(self.page, "Upload"),
                        UploadFile(self.page),
                    ],
                )
            )
        self.page.update()

    def view_pop(self, view):
        print("View pop:", view)
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)

