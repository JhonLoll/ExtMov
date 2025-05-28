import flet as ft

class UploadFile(ft.Column):
    def __init__(self, page: ft.Page):
        self.page = page

        # ===================================
        # Inicializa o FilePicker com Overlay
        self.file_picker = ft.FilePicker(
            on_result=self.file_picked
        )

        self.page.overlay.append(self.file_picker)

        # ===================================
        # Inicializa os controles de Texto
        self.tile_text = ft.Text("Upload de Arquivo")
        self.label_text = ft.Text("Selecione o arquivo:")

        # ===================================
        # Inicializa o botão de Upload
        self.upload_button = ft.ElevatedButton(
            "Escolher arquivo", 
            icon=ft.Icons.UPLOAD_FILE,
            on_click= lambda e: self.file_picker.pick_files(
                allow_multiple=True,
            )
        )

        # ======================================
        # Container dos arquivos selecionados
        self.selected_files = ft.Text(
            "Nenhum arquivo selecionado.",
            style=ft.TextStyle(
                size=12,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLACK,
            )
        )

        self.file_container = ft.Container(
            content=self.selected_files,
            padding=10,
            alignment=ft.alignment.center,
            width=300,
            height=200,
            border_radius=ft.border_radius.all(10),
        )

        # ======================================
        # Inicializa a coluna principal
        super().__init__(
            controls=[
                self.tile_text,
                self.label_text,
                self.upload_button,
                self.file_container,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=15,
        )

    def file_picked(self, e: ft.FilePickerResultEvent):
        # Atualiza o texto com os arquivos selecionados
        self.selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Nenhum arquivo selecionado."
        )
        self.selected_files.update()
