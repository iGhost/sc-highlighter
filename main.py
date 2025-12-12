import tkinter as tk
from tkinter import scrolledtext
from pathlib import Path
import threading
import tempfile
import shutil
import os

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 600
BUTTON_WIDTH_PX = 130
BUTTON_HEIGHT_PX = 35

# Paths
HIGHLIGHT_FILE = "highlight.txt"
INI_FILE = "global.ini"
BACKUP_DIR = "_backup"

def load_highlight():
    """TODO: Should surround labels with tags"""
    try:
        with open(HIGHLIGHT_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error loading {HIGHLIGHT_FILE}: {e}")
        return ""

def thread_highlight():
    """Highlight button: Run replacement function."""
    def task():
        content = thread_highlight_run()
        print("Highlight file contents:")
        print(content)
    threading.Thread(target=task, daemon=True).start()

def thread_highlight_run():
    """Highlight button: Run replacement function."""
    source_file = Path(INI_FILE)
    try:
        input_lines = []
        with open(HIGHLIGHT_FILE, "r", encoding="utf-8") as f:
            input_lines = f.readlines()
        input_lines = list(map(lambda l: l.strip().split('=')[0], input_lines))

        with tempfile.NamedTemporaryFile('w', dir=source_file.parent, delete=False, encoding='utf-8') as tmp:
            temp_file = Path(tmp.name)
            with open(source_file, encoding='utf-8') as global_file:
                for line in global_file:
                    for pattern in input_lines:
                        if line.startswith(pattern):
                            line = line.split('=', 1)
                            line = f"{line[0]}=<EM1>{line[1].strip()}</EM1>\n"
                            break
                    tmp.write(line)
        os.replace(temp_file, INI_FILE)
        return True
    except Exception as e:
        print(f"Error loading files: {e}")
        return False

def backup_thread():
    """Backup button: copy INI_FILE to BACKUP_DIR."""
    def task():
        try:
            os.makedirs(BACKUP_DIR, exist_ok=True)
            src = INI_FILE
            dst = os.path.join(BACKUP_DIR, INI_FILE)
            shutil.copy2(src, dst)
            print(f"Backed up {INI_FILE} to {dst}")
        except Exception as e:
            print(f"Backup failed: {e}")
    threading.Thread(target=task, daemon=True).start()

def restore_thread():
    """Restore button: copy INI_FILE from BACKUP_DIR."""
    def task():
        try:
            src = os.path.join(BACKUP_DIR, INI_FILE)
            dst = INI_FILE
            shutil.copy2(src, dst)
            print(f"Restored {INI_FILE} from {src}")
        except Exception as e:
            print(f"Restore failed: {e}")
    threading.Thread(target=task, daemon=True).start()

def main():
    root = tk.Tk()
    root.minsize(338, 338)
    root.title("Star Citizen Label Highlighter")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
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
    initial_text = load_highlight()
    txt_area.insert(tk.END, initial_text)
    txt_area.config(state=tk.DISABLED)

    # Button and callbacks
    btn_highlight = tk.Button(button_frame,
                              text="Highlight",
                              width=BUTTON_WIDTH_PX // 10,
                              height=BUTTON_HEIGHT_PX // 20,
                              command=thread_highlight,
                              bg="#4A4A4A", fg="white", activebackground="#6A6A6A", activeforeground="white",
                              font=('Arial', 10, 'bold'))
    btn_highlight.pack(side=tk.LEFT)

    btn_restore = tk.Button(button_frame,
                            text="Restore",
                            width=BUTTON_WIDTH_PX // 10,
                            height=BUTTON_HEIGHT_PX // 20,
                            command=restore_thread,
                            bg="#4A4A4A", fg="white", activebackground="#6A6A6A", activeforeground="white")
    btn_restore.pack(side=tk.RIGHT)

    btn_backup = tk.Button(button_frame,
                           text="Backup",
                           width=BUTTON_WIDTH_PX // 10,
                           height=BUTTON_HEIGHT_PX // 20,
                           command=backup_thread,
                           bg="#4A4A4A", fg="white", activebackground="#6A6A6A", activeforeground="white")
    btn_backup.pack(side=tk.RIGHT)

    root.mainloop()

if __name__ == "__main__":
    main()
