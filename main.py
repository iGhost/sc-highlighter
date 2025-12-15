import tkinter as tk
from tkinter import scrolledtext
from pathlib import Path
import threading
import tempfile
import shutil
import os


class App:
    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 600
    BUTTON_WIDTH_PX = 130
    BUTTON_HEIGHT_PX = 35

    # Paths
    HIGHLIGHT_FILE = "highlight.txt"
    INI_FILE = "global.ini"
    INI_FILE_PATH = "data\\Localization\\korean_(south_korea)"
    BACKUP_DIR = "_backup"

    global_buttons = {}

    def load_highlight(self):
        try:
            with open(self.HIGHLIGHT_FILE, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error loading {self.HIGHLIGHT_FILE}: {e}")
            return ""

    def thread_highlight(self):
        """Highlight button: Run replacement function."""
        def task():
            content = self.thread_highlight_run()
            if content:
                print('Done successfully')
                self.flash(self.global_buttons['highlight'], color='green')
            else:
                print('Failed')
        threading.Thread(target=task, daemon=True).start()

    def thread_highlight_run(self):
        """Highlight button: Run replacement function."""
        source_file = Path(os.path.join(self.INI_FILE_PATH, self.INI_FILE))
        try:
            input_lines = []
            with open(self.HIGHLIGHT_FILE, "r", encoding="utf-8") as f:
                input_lines = f.readlines()
            input_lines = list(map(lambda l: l.strip().split('=')[0], input_lines))

            with tempfile.NamedTemporaryFile('w', dir=source_file.parent, delete=False, encoding='utf-8') as tmp:
                temp_file = Path(tmp.name)
                with open(source_file, encoding='utf-8') as global_file:
                    for line in global_file:
                        line_dict = line.split('=', 1)
                        for pattern in input_lines:
                            if line_dict[0] == pattern:
                                line = f"{line_dict[0]}=<EM1>{line_dict[1].strip()}</EM1>\n"
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
                print(f"Backed up {self.INI_FILE} ({src}) to {dst}")
            except Exception as e:
                print(f"Backup failed: {e}")
        threading.Thread(target=task, daemon=True).start()

    def restore_thread(self):
        """Restore button: copy INI_FILE from BACKUP_DIR."""
        def task():
            try:
                src = os.path.join(self.BACKUP_DIR, self.INI_FILE)
                dst = os.path.join(self.INI_FILE_PATH, self.INI_FILE)
                shutil.copy2(src, dst)
                print(f"Restored {self.INI_FILE} from {src}||{dst}")
            except Exception as e:
                print(f"Restore failed: {e}")
        threading.Thread(target=task, daemon=True).start()

    def flash(self, widget: tk.Widget, color: str, duration: int = 1000):
        old_bg = widget.cget("bg")
        widget.config(bg=color)
        widget.after(duration, lambda: widget.config(bg=old_bg))

    def main(self):
        root = tk.Tk()
        root.minsize(338, 338)
        root.title("Star Citizen Label Highlighter")
        root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        root.configure(bg="#2E2E2E")  # Dark grey
        root.bind('<Escape>', lambda e, w=root: w.destroy())

        # Left frame for buttons
        button_frame = tk.Frame(root, bg="#2E2E2E")
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Right frame for text area
        text_frame = tk.Frame(root, bg="#2E2E2E")
        text_frame.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Text area with scroll
        txt_area = scrolledtext.ScrolledText(text_frame, wrap='none', bg="#4A4A4A", fg="#CCCCCC")
        txt_area.pack(expand=True, fill=tk.BOTH)

        # Load highlight.txt into text area
        initial_text = self.load_highlight()
        txt_area.insert(tk.END, initial_text)
        txt_area.config(state=tk.DISABLED)

        # Button and callbacks
        btn_highlight = tk.Button(button_frame,
                                  text="Highlight",
                                  width=self.BUTTON_WIDTH_PX // 10,
                                  height=self.BUTTON_HEIGHT_PX // 20,
                                  command=self.thread_highlight,
                                  bg="#4A4A4A", fg="white", activebackground="#6A6A6A", activeforeground="white",
                                  font=('Arial', 10, 'bold'))
        btn_highlight.pack(side=tk.LEFT)

        btn_restore = tk.Button(button_frame,
                                text="Restore",
                                width=self.BUTTON_WIDTH_PX // 10,
                                height=self.BUTTON_HEIGHT_PX // 20,
                                command=self.restore_thread,
                                bg="#4A4A4A", fg="white", activebackground="#6A6A6A", activeforeground="white")
        btn_restore.pack(side=tk.RIGHT)

        btn_backup = tk.Button(button_frame,
                               text="Backup",
                               width=self.BUTTON_WIDTH_PX // 10,
                               height=self.BUTTON_HEIGHT_PX // 20,
                               command=self.backup_thread,
                               bg="#4A4A4A", fg="white", activebackground="#6A6A6A", activeforeground="white")
        btn_backup.pack(side=tk.RIGHT)

        self.global_buttons = {
            'highlight': btn_highlight,
            'restore': btn_restore,
            'backup': btn_backup
        }

        root.mainloop()

if __name__ == "__main__":
    app = App()
    app.main()
