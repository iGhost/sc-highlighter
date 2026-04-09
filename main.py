import tkinter as tk
from tkinter import ttk
from pathlib import Path
from src.version import __version__
import webbrowser
import threading
import tempfile
import shutil
import sys
import os


class App:
    WINDOW_WIDTH = 520
    WINDOW_HEIGHT = 600
    BUTTON_WIDTH = 15
    BUTTON_HEIGHT_PX = 35
    DEFAULT_EM_TAG = 4
    colors_dict = {
        1: "Blue",
        2: "Green",
        3: "Yellow",
        4: "Red",
    }

    # Paths
    HIGHLIGHT_FILE = "my_items.txt"
    HIGHLIGHT_DIR = "highlights"
    INI_FILE = "global.ini"
    INI_FILE_PATH = "data\\Localization\\korean_(south_korea)"
    BACKUP_DIR = "_backup"

    def __init__(self):
        self.root = None
        self.buttons = {}
        self.txt_area = None
        self.text_files = []
        self.colors_combo = None
        self.file_list_canvas = None
        self.file_list_scrollbar = None
        self.file_list_inner = None
        self.file_list_window = None
        self.file_list_scrollbar_visible = False

    def count_lines(self, file_path: Path) -> int:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return sum(1 for l in f if l.strip() != '')
        except:
            return 0

    def preload_files(self):
        load_dir = Path(self.HIGHLIGHT_DIR)
        os.makedirs(load_dir, exist_ok=True)
        self.text_files = [str(p) for p in load_dir.glob("*.txt") if p.is_file()]
        if len(self.text_files) > 0:
            checkbox_state = True if len(self.text_files) == 1 else False
            self.text_files = list(
                map(lambda f: {'file': f, 'lines': self.count_lines(f), 'tag': self.DEFAULT_EM_TAG,
                               'check': tk.BooleanVar(value=checkbox_state)}, self.text_files))
            for item in self.text_files:
                if item['file'].endswith(self.HIGHLIGHT_FILE):
                    item['check'] = tk.BooleanVar(value=True)
        else:
            new_file = os.path.join(load_dir, self.HIGHLIGHT_FILE)
            with open(new_file, "w", encoding="utf-8") as f:
                f.write("items_commodities_carinite_pure\nitems_commodities_carinite_raw")
            self.text_files = [{'file': new_file, 'lines': 2, 'tag': self.DEFAULT_EM_TAG, 'check': tk.BooleanVar(value=True)}]
        print(f"Found text files: {len(self.text_files)}")

    def create_file_checkboxes(self, frame):
        for i, file in enumerate(self.text_files):
            checkbox = tk.Checkbutton(
                frame, text=f"{file['file']}  ({file['lines']})", variable=self.text_files[i]['check'],
                selectcolor="#2E2E2E", activebackground="#6A6A6A", activeforeground="#CCCCCC",
                bg="#2E2E2E", fg="#CCCCCC",
            )
            checkbox.pack(anchor="nw", padx=5, pady=1)

    def create_scrollable_file_list(self, parent):
        self.file_list_canvas = tk.Canvas(parent, bg="#2E2E2E", highlightthickness=0, borderwidth=0)
        self.file_list_canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.file_list_scrollbar = tk.Scrollbar(parent, orient=tk.VERTICAL, command=self.file_list_canvas.yview)
        self.file_list_canvas.configure(yscrollcommand=self.file_list_scrollbar.set)

        self.file_list_inner = tk.Frame(self.file_list_canvas, bg="#2E2E2E")
        self.file_list_window = self.file_list_canvas.create_window((0, 0), window=self.file_list_inner, anchor="nw")

        self.file_list_inner.bind("<Configure>", self.update_file_list_scrollregion)
        self.file_list_canvas.bind("<Configure>", self.on_file_list_canvas_configure)
        self.file_list_canvas.bind("<MouseWheel>", self.on_file_list_mousewheel)
        self.file_list_inner.bind("<MouseWheel>", self.on_file_list_mousewheel)

        self.create_file_checkboxes(self.file_list_inner)
        self.update_file_list_scrollbar()

    def update_file_list_scrollregion(self, _event=None):
        self.file_list_canvas.configure(scrollregion=self.file_list_canvas.bbox("all"))
        self.update_file_list_scrollbar()

    def on_file_list_canvas_configure(self, event):
        self.file_list_canvas.itemconfigure(self.file_list_window, width=event.width)
        self.update_file_list_scrollbar()

    def on_file_list_mousewheel(self, event):
        if not self.file_list_canvas or not self.file_list_scrollbar_visible:
            return

        self.file_list_canvas.yview_scroll(int(-event.delta / 120), "units")

    def update_file_list_scrollbar(self):
        if not self.file_list_canvas or not self.file_list_scrollbar or not self.file_list_inner:
            return

        scroll_region = self.file_list_canvas.bbox("all")
        content_height = scroll_region[3] - scroll_region[1] if scroll_region else 0
        viewport_height = self.file_list_canvas.winfo_height()
        needs_scrollbar = content_height > viewport_height

        if needs_scrollbar and not self.file_list_scrollbar_visible:
            self.file_list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.file_list_scrollbar_visible = True
        elif not needs_scrollbar and self.file_list_scrollbar_visible:
            self.file_list_scrollbar.pack_forget()
            self.file_list_scrollbar_visible = False

    def thread_highlight(self):
        """Highlight button: Run replacement function in thread."""
        def task():
            content = self.thread_highlight_run()
            if content:
                print('Replaced successfully')
                self.flash(self.buttons['highlight'], color='green')
            else:
                print('Replacement failed')
                self.flash(self.buttons['highlight'], color='red')
        threading.Thread(target=task, daemon=True).start()

    def thread_highlight_run(self):
        """Replacement function."""
        color_to_key = {v: k for k, v in self.colors_dict.items()}

        source_file = Path(os.path.join(self.INI_FILE_PATH, self.INI_FILE))
        try:
            tag_number = color_to_key[self.colors_combo.get()]
            input_lines = []
            for file in [f for f in self.text_files if f['check'].get()]:
                with open(file['file'], "r", encoding="utf-8") as f:
                    input_lines.extend([l.strip() for l in f if l.strip() != ''])
            input_lines = list(set(map(lambda l: l.split('=')[0], input_lines)))
            print(f"Extracted {len(input_lines)} lines")

            with tempfile.NamedTemporaryFile('w', dir=source_file.parent, delete=False, encoding='utf-8') as tmp:
                temp_file = Path(tmp.name)
                with open(source_file, encoding='utf-8') as global_file:
                    for line in global_file:
                        line_dict = line.split('=', 1)
                        for pattern in input_lines:
                            if line_dict[0] == pattern:
                                line = f"{line_dict[0]}=<EM{tag_number}>{line_dict[1].strip()}</EM{tag_number}>\n"
                                break
                        tmp.write(line)
            os.replace(temp_file, source_file)
            return True
        except Exception as e:
            print(f"Error loading files: {e}")
            return False

    def backup_thread(self):
        """Backup button: copy INI_FILE to BACKUP_DIR."""
        def task():
            try:
                os.makedirs(self.BACKUP_DIR, exist_ok=True)
                src = os.path.join(self.INI_FILE_PATH, self.INI_FILE)
                dst = os.path.join(self.BACKUP_DIR, self.INI_FILE)
                shutil.copy2(src, dst)
                print(f"Backed up \"{self.INI_FILE}\" (\"{src}\") to \"{dst}\"")
                self.flash(self.buttons['backup'], color='green')
            except Exception as e:
                print(f"Backup failed: {e}")
                self.flash(self.buttons['backup'], color='red')
        threading.Thread(target=task, daemon=True).start()

    def restore_thread(self):
        """Restore button: copy INI_FILE from BACKUP_DIR."""
        def task():
            try:
                src = os.path.join(self.BACKUP_DIR, self.INI_FILE)
                dst = os.path.join(self.INI_FILE_PATH, self.INI_FILE)
                shutil.copy2(src, dst)
                print(f"Restored \"{self.INI_FILE}\" (\"{src}\") to \"{dst}\"")
                self.flash(self.buttons['restore'], color='green')
            except Exception as e:
                print(f"Restore failed: {e}")
                self.flash(self.buttons['restore'], color='red')
        threading.Thread(target=task, daemon=True).start()

    def flash(self, widget: tk.Widget, color: str, duration: int = 1000):
        """Flash specified button with specified color"""
        old_bg = widget.cget("bg")
        widget.config(bg=color)
        widget.after(duration, lambda: widget.config(bg=old_bg))

    def send_to_url(self, url):
        webbrowser.open_new(url)

    def create_buttons(self, parent):
        """Create all buttons and add to global_buttons dictionary."""
        btn_highlight = tk.Button(parent,
                                  text="Highlight",
                                  width=self.BUTTON_WIDTH,
                                  height=self.BUTTON_HEIGHT_PX // 20,
                                  command=self.thread_highlight,
                                  bg="#4A4A4A", fg="white", activebackground="#6A6A6A", activeforeground="white",
                                  font=('Arial', 10, 'bold'))
        btn_highlight.pack(side=tk.LEFT)

        btn_restore = tk.Button(parent,
                                text="Restore global.ini",
                                width=self.BUTTON_WIDTH,
                                height=self.BUTTON_HEIGHT_PX // 20,
                                command=self.restore_thread,
                                bg="#4A4A4A", fg="white", activebackground="#6A6A6A", activeforeground="white")
        btn_restore.pack(side=tk.RIGHT)

        btn_backup = tk.Button(parent,
                               text="Backup global.ini",
                               width=self.BUTTON_WIDTH,
                               height=self.BUTTON_HEIGHT_PX // 20,
                               command=self.backup_thread,
                               bg="#4A4A4A", fg="white", activebackground="#6A6A6A", activeforeground="white")
        btn_backup.pack(side=tk.RIGHT, padx=5)

        self.buttons = {
            'highlight': btn_highlight,
            'restore': btn_restore,
            'backup': btn_backup
        }

    def create_second_row(self, parent):
        lbl_link_discord = tk.Label(parent, text="Discord 🔗", cursor="hand2",
                               bg="#2E2E2E", fg="white", activebackground="#6A6A6A", activeforeground="white")
        lbl_link_discord.pack(side=tk.RIGHT, padx=5)
        lbl_link_discord.bind("<Button-1>", lambda e: self.send_to_url("https://discord.gg/3VVJ8vRKpr"))

        lbl_link_site = tk.Label(parent, text="Site 🔗", cursor="hand2",
                               bg="#2E2E2E", fg="white", activebackground="#6A6A6A", activeforeground="white")
        lbl_link_site.pack(side=tk.RIGHT, padx=5)
        lbl_link_site.bind("<Button-1>", lambda e: self.send_to_url("https://www.expanseunion.com/sc/expanseutility"))

        self.colors_combo = ttk.Combobox(parent, values=list(self.colors_dict.values()), state="readonly", width=17)
        self.colors_combo.pack(side=tk.LEFT, padx=5, pady=5)
        self.colors_combo.current(3)

    def main(self):
        self.current_version = __version__
        self.root = tk.Tk()
        self.root.minsize(392, 338)
        self.root.title(f"Highlight My Items v{self.current_version} | Expanse Utility от людей в тапках")
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.root.configure(bg="#2E2E2E")
        self.root.bind('<Escape>', lambda e, w=self.root: w.destroy())

        if getattr(sys, "frozen", False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        try:
            self.root.iconbitmap(os.path.join(base_path, "assets", "icon.ico"))
        except tk.TclError:
            print("Warning: Could not load icon file")

        # Top frame for buttons
        button_frame = tk.Frame(self.root, bg="#2E2E2E")
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 0))

        # Second row frame for combobox and links
        second_frame = tk.Frame(self.root, bg="#2E2E2E", borderwidth=2, relief="flat", height=35)
        second_frame.pack(side=tk.TOP, expand=False, fill=tk.BOTH, padx=4, pady=0)
        second_frame.pack_propagate(False)

        # Bottom frame for file list
        text_frame = tk.Frame(self.root, bg="#2E2E2E", borderwidth=2, relief="sunken")
        text_frame.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH, padx=10, pady=(0, 10))

        self.create_buttons(button_frame)
        self.create_second_row(second_frame)
        self.preload_files()
        self.create_scrollable_file_list(text_frame)

        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.main()
