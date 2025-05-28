import os
import flet as ft

from pages.route import Routing


def main(page: ft.Page):
    
    # Configuração da página
    page.title = "Extrato de Movimentação"
    page.window.width = 1000
    page.window.height = 600
    page.theme = ft.Theme(color_scheme_seed="#6da485")
    page.theme.page_transitions.windows = "cupertino"
    page.theme_mode = ft.ThemeMode.DARK

    # Classe Routing - Responsável por gerenciar as rotas da aplicação
    router = Routing(page)

    # Inicia na página inicial
    page.go("/")

ft.app(target=main, upload_dir=f"{os.path.join(os.getcwd(), os.path.join("src", "temp") if os.path.exists("src") else os.path.join("temp"))}")
