import subprocess
import os
import threading
from textual.app import App, ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Button, TextArea, RichLog, RadioSet, RadioButton, Label, ListView, ListItem                                              
from textual.containers import Horizontal, Vertical, Grid

TEMPLATE_HELLO_WORLD = "begin\n  writeln('Hello World');\nend."
TEMPLATE_EMPTY = "begin\n  \nend."

# ==========================================================                                                  
# ДИНАМИЧЕСКОЕ ОПРЕДЕЛЕНИЕ ПУТЕЙ (Умная автоматика)
# ==========================================================                                                  
# Находим папку, в которой физически лежит этот файл tui.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Путь к компилятору прямо в этой же папке
COMPILER_PATH = os.path.join(BASE_DIR, "pabcnetc.exe")

# Путь к папке с проектами
PROJECTS_DIR = os.path.join(BASE_DIR, "Projects")
# ==========================================================

class FileMenuScreen(ModalScreen):
    """Экран модального меню со списком файлов"""

    CSS = """
    FileMenuScreen {
        align: center middle;
        background: rgba(0, 0, 0, 0.5);
    }
    #menu_container {
        width: 40;
        height: 70%;
        background: $panel;
        border: thick $primary;
        padding: 1;
    }
    #menu_file_list {
        background: $surface;
        border: solid $primary;
        height: 1fr;
        margin-top: 1;
        margin-bottom: 1;
    }
    .menu_btn {
        width: 100%;
        margin-bottom: 1;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="menu_container"):
            yield Label("📁 ВЫБОР ПРОЕКТА:")

            initial_items = []
            if os.path.exists(PROJECTS_DIR):
                files = [f for f in os.listdir(PROJECTS_DIR) if f.endswith(".pas")]
                files.sort()
                for file in files:
                    safe_id = f"file_{file.replace('.', '_')}"
                    initial_items.append(ListItem(Label(f"📄 {file}"), id=safe_id))

            yield ListView(*initial_items, id="menu_file_list")
            yield Button("➕ Новый файл", variant="primary", id="menu_create_btn", classes="menu_btn")
            yield Button("🗑️ Удалить выбранный", variant="error", id="menu_delete_btn", classes="menu_btn")
            yield Button("❌ Закрыть меню", variant="default", id="menu_close_btn", classes="menu_btn")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.item and event.item.id:
            self.dismiss(("select", event.item.id))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "menu_close_btn":
            self.dismiss(None)
        elif event.button.id == "menu_create_btn":
            self.dismiss(("create", True))
        elif event.button.id == "menu_delete_btn":
            file_list = self.query_one("#menu_file_list", ListView)
            if file_list.highlighted_child and file_list.highlighted_child.id:
                self.dismiss(("delete", file_list.highlighted_child.id))


class PascalTUI(App):                                  
    BINDINGS = [
        ("q", "quit", "Выйти"),
        ("o", "open_menu", "Открыть меню проектов"),
        ("s", "toggle_settings", "Настройки")
    ]

    CSS = """
    #main_layout {
        layout: vertical;
    }
    #workspace {
        height: 1fr;
    }
    #buttons_container {
        height: 3;
        margin-top: 1;
        margin-bottom: 1;
    }
    Button {
        margin-right: 1;
    }
    #settings_panel {
        border: solid green;
        background: $surface;
        padding: 1;
        display: none;
        height: auto;
        margin-bottom: 1;
    }
    """

    def __init__(self):
        super().__init__()
        self.code_backup = ""
        self.current_file = os.path.join(PROJECTS_DIR, "main.pas")

        if not os.path.exists(PROJECTS_DIR):
            os.makedirs(PROJECTS_DIR)

        if not os.listdir(PROJECTS_DIR):
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(TEMPLATE_HELLO_WORLD)

    def load_start_code(self) -> str:
        if os.path.exists(self.current_file):
            with open(self.current_file, "r", encoding="utf-8") as f:
                return f.read()
        return TEMPLATE_HELLO_WORLD

    def save_current_file(self) -> None:
        """Автоматическое сохранение текущего открытого файла"""
        if hasattr(self, 'current_file') and self.current_file:
            try:
                with open(self.current_file, "w", encoding="utf-8") as f:
                    f.write(self.editor.text)
            except Exception:
                pass

    def compose(self) -> ComposeResult:                
        yield Header(show_clock=True)                  

        with Vertical(id="main_layout"):
            with Vertical(id="workspace"):
                yield Label("Активен: " + os.path.basename(self.current_file), id="cur_file_lbl")

                start_code = self.load_start_code()
                self.editor = TextArea(start_code, language="pascal")
                yield self.editor                      

                with Horizontal(id="buttons_container"):
                    yield Button("📁 Проекты (O)", variant="primary", id="open_menu_btn")
                    yield Button("Запустить", variant="success", id="run_btn")                                
                    yield Button("Настройки", variant="default", id="settings_btn")

                with Vertical(id="settings_panel"):
                    yield RadioSet(
                        RadioButton("Стартовать с Hello World", id="set_hello", value=True),
                        RadioButton("Стартовать с пустого шаблона", id="set_empty", value=False),
                        id="template_radio"
                    )
                    with Horizontal():
                        yield Button("Стереть весь код", variant="error", id="clear_btn")
                        yield Button("Восстановить", variant="warning", id="undo_btn")

                self.log_box = RichLog()               
                yield self.log_box                     
        yield Footer()                                                                                        

    def action_open_menu(self) -> None:
        """Открытие модального окна с меню файлов"""
        self.save_current_file()
        self.push_screen(FileMenuScreen(), self.handle_menu_result)

    def handle_menu_result(self, result: tuple) -> None:
        """Обработка действий, совершённых в меню проектов"""
        if not result:
            return

        action_type, data = result

        if action_type == "select":
            filename = data.replace("file_", "").replace("_pas", ".pas")
            self.current_file = os.path.join(PROJECTS_DIR, filename)
            with open(self.current_file, "r", encoding="utf-8") as f:
                self.editor.text = f.read()
            self.query_one("#cur_file_lbl").update("Активен: " + filename)
            self.log_box.write(f"[Открыт файл: {filename}]\n")

        elif action_type == "create":
            count = 1
            while os.path.exists(os.path.join(PROJECTS_DIR, f"project_{count}.pas")):
                count += 1
            new_filename = f"project_{count}.pas"
            self.current_file = os.path.join(PROJECTS_DIR, new_filename)

            # Проверяем радио-кнопку настроек для выбора шаблона нового файла
            radio_hello = self.query_one("#set_hello", RadioButton)
            chosen_template = TEMPLATE_HELLO_WORLD if radio_hello.value else TEMPLATE_EMPTY

            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(chosen_template)

            self.editor.text = chosen_template
            self.query_one("#cur_file_lbl").update("Активен: " + new_filename)
            self.log_box.write(f"[Создан файл: {new_filename}]\n")
            self.action_open_menu()

        elif action_type == "delete":
            filename = data.replace("file_", "").replace("_pas", ".pas")
            target_path = os.path.join(PROJECTS_DIR, filename)

            if os.path.exists(target_path):
                os.remove(target_path)
                exe_p = os.path.splitext(target_path)[0] + ".exe"
                if os.path.exists(exe_p): os.remove(exe_p)

                self.log_box.write(f"[Файл {filename} удален]\n")

                remaining_files = [f for f in os.listdir(PROJECTS_DIR) if f.endswith(".pas")]
                if remaining_files:
                    self.current_file = os.path.join(PROJECTS_DIR, remaining_files[0])
                else:
                    self.current_file = os.path.join(PROJECTS_DIR, "main.pas")
                    with open(self.current_file, "w", encoding="utf-8") as f:
                        f.write(TEMPLATE_HELLO_WORLD)

                with open(self.current_file, "r", encoding="utf-8") as f:
                    self.editor.text = f.read()

                self.query_one("#cur_file_lbl").update("Активен: " + os.path.basename(self.current_file))
            self.action_open_menu()

    def on_button_pressed(self, event: Button.Pressed) -> None:                                               
        if event.button.id == "open_menu_btn":
            self.action_open_menu()

        elif event.button.id == "run_btn":             
            self.log_box.clear()                                                                              
            self.save_current_file()                                                                          

            base_name = os.path.splitext(self.current_file)[0]
            exe_path = base_name + ".exe"

            if os.path.exists(exe_path):               
                os.remove(exe_path)                                                                           

            self.log_box.write(f"Компиляция {os.path.basename(self.current_file)}...\n")                                                                             

            # ИСПОЛЬЗУЕМ ДИНАМИЧЕСКИЙ ПУТЬ К КОМПИЛЯТОРУ
            if not os.path.exists(COMPILER_PATH):
                self.log_box.write(f"[ОШИБКА] Компилятор не найден по пути:\n{COMPILER_PATH}\n")
                return

            res = subprocess.run(["mono", COMPILER_PATH, self.current_file], capture_output=True, text=True)                                                         

            if "Lines compiled:" in res.stdout or ("OK" in res.stdout and "Compiling assembly" in res.stdout):
                self.log_box.write("[Скомпилировано успешно! Запуск...]\n")
                
                # Замораживаем интерфейс Textual и открываем чистый Термукс для работы ввода
                with self.suspend():
                    import os as native_os    
                    native_os.system('clear') 
                    print(f"=== ЗАПУСК ПРОГРАММЫ ===")
                    print(f"Выполняется файл: {os.path.basename(exe_path)}\n------------------------")
                    
                    # Прямой интерактивный запуск через родной Термукс
                    native_os.system(f"mono {exe_path}")
                    
                    print("\n------------------------")
                    input("Программа завершена. Нажмите Enter, чтобы вернуться в IDE...")
            else:                                      
                self.log_box.write("[Ошибка компиляции!]\n")                                                  
                self.log_box.write(res.stdout)         
                self.log_box.write(res.stderr)         

        elif event.button.id == "settings_btn":
            self.action_toggle_settings()
        elif event.button.id == "clear_btn":
            self.code_backup = self.editor.text
            self.editor.text = "begin\n  \nend."
        elif event.button.id == "undo_btn":
            if self.code_backup: self.editor.text = self.code_backup

    def action_toggle_settings(self) -> None:
        panel = self.query_one("#settings_panel")
        panel.styles.display = "none" if panel.styles.display == "block" else "block"

if __name__ == "__main__":                             
    PascalTUI().run()

