import tkinter as tk
from tkinter import scrolledtext
import threading
import shutil
import os

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 600
BUTTON_WIDTH_PX = 130
BUTTON_HEIGHT_PX = 35

# Paths
HIGHLIGHT_FILE = "highlight.txt"
INI_FILE = "global-small.ini"
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
        content = load_highlight()
        print("Highlight file contents:")
        print(content)
    threading.Thread(target=task, daemon=True).start()

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
    root.title("Star Citizen Label Highlighter")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.configure(bg="#2E2E2E")  # Dark grey

    # Left frame for buttons
    button_frame = tk.Frame(root, bg="#2E2E2E")
    button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    # Right frame for text area
    text_frame = tk.Frame(root, bg="#2E2E2E")
    text_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)

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
                              bg="#4A4A4A", fg="white", activebackground="#6A6A6A", activeforeground="white")
    btn_highlight.pack(pady=5)

    btn_backup = tk.Button(button_frame,
                           text="Backup",
                           width=BUTTON_WIDTH_PX // 10,
                           height=BUTTON_HEIGHT_PX // 20,
                           command=backup_thread,
                           bg="#4A4A4A", fg="white", activebackground="#6A6A6A", activeforeground="white")
    btn_backup.pack(pady=5)

    btn_restore = tk.Button(button_frame,
                            text="Restore",
                            width=BUTTON_WIDTH_PX // 10,
                            height=BUTTON_HEIGHT_PX // 20,
                            command=restore_thread,
                            bg="#4A4A4A", fg="white", activebackground="#6A6A6A", activeforeground="white")
    btn_restore.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
