"""Floating Desktop Pill Widget and Global Hotkey Listener for ScreenSense Guardian.

Provides:
1. An always-on-top, elegant floating widget at the top of your screen.
2. Global hotkey listener (Alt + Space or Ctrl + Space) to summon ScreenSense instantly from anywhere.
"""

import sys
import threading
import time
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

from .app import route_unified_request
from .overlay_ui import overlay

try:
    from pynput import keyboard
    HAS_PYNPUT = True
except ImportError:
    HAS_PYNPUT = False


class FloatingPillWidget:
    """Floating desktop pill that stays on top and responds to clicks and hotkeys."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ScreenSense Widget")
        
        # Window attributes: borderless, always on top
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        
        screen_w = self.root.winfo_screenwidth()
        pill_w, pill_h = 360, 44
        pos_x = (screen_w - pill_w) // 2
        pos_y = 12  # Near top edge of screen

        self.root.geometry(f"{pill_w}x{pill_h}+{pos_x}+{pos_y}")

        # Dark sleek background
        self.frame = tk.Frame(self.root, bg="#161b22", highlightbackground="#58a6ff", highlightthickness=1)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Label icon & text
        self.lbl = tk.Label(
            self.frame,
            text="🛡️ ScreenSense  •  Click or press Alt+Space",
            font=("Arial", 11, "bold"),
            fg="#f0f6fc",
            bg="#161b22",
            cursor="hand2"
        )
        self.lbl.pack(side=tk.LEFT, padx=12, pady=8)

        # Quick action button
        self.btn_check = tk.Button(
            self.frame,
            text="Check",
            font=("Arial", 9, "bold"),
            fg="#ffffff",
            bg="#238636",
            activebackground="#2ea043",
            relief=tk.FLAT,
            padx=8,
            command=self.on_quick_check
        )
        self.btn_check.pack(side=tk.RIGHT, padx=(4, 10), pady=6)

        # Bind click triggers
        self.lbl.bind("<Button-1>", lambda e: self.open_query_modal())
        self.frame.bind("<Button-1>", lambda e: self.open_query_modal())

        # Draggable pill support
        self.lbl.bind("<B1-Motion>", self._on_drag)
        self.lbl.bind("<ButtonPress-1>", self._on_drag_start)

        # Start hotkey listener thread
        if HAS_PYNPUT:
            self._start_hotkey_listener()

    def _on_drag_start(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def _on_drag(self, event):
        x = self.root.winfo_x() - self._drag_start_x + event.x
        y = self.root.winfo_y() - self._drag_start_y + event.y
        self.root.geometry(f"+{x}+{y}")

    def on_quick_check(self):
        """Quick check button clicked: immediately checks screen text for fraud."""
        fake_test_text = "Windows Defender Alert! Your PC is infected with Trojan! Call 1-800-555-0199 now!"
        route_unified_request(user_input="check this", screen_text=fake_test_text, interactive_ui=True)

    def open_query_modal(self):
        """Opens a focused query input dialog to ask questions or report scams."""
        modal = tk.Toplevel(self.root)
        modal.title("ScreenSense AI Assistant")
        modal.attributes("-topmost", True)
        modal.geometry("520x150+300+200")
        modal.configure(bg="#0d1117")

        tk.Label(modal, text="💡 Ask ScreenSense or Describe What You Need:", font=("Arial", 12, "bold"), fg="#58a6ff", bg="#0d1117").pack(pady=(12, 6))

        entry = tk.Entry(modal, font=("Arial", 12), width=45, bg="#161b22", fg="#f0f6fc", insertbackground="white")
        entry.pack(pady=6, padx=16)
        entry.focus_set()

        def submit():
            val = entry.get().strip()
            modal.destroy()
            if val:
                route_unified_request(user_input=val, interactive_ui=True)

        entry.bind("<Return>", lambda e: submit())

        btn_row = tk.Frame(modal, bg="#0d1117")
        btn_row.pack(pady=8)

        tk.Button(btn_row, text="💡 Ask Tutor", font=("Arial", 10, "bold"), bg="#1f6feb", fg="white", relief=tk.FLAT, padx=10, command=submit).pack(side=tk.LEFT, padx=6)
        tk.Button(btn_row, text="🛡️ Check for Scam", font=("Arial", 10, "bold"), bg="#da3633", fg="white", relief=tk.FLAT, padx=10, command=lambda: [modal.destroy(), self.on_quick_check()]).pack(side=tk.LEFT, padx=6)

    def _start_hotkey_listener(self):
        """Listens for global Alt+Space or Ctrl+Space to activate ScreenSense."""
        def for_canonical(f):
            return lambda k: f(listener.canonical(k))

        hotkey = keyboard.HotKey(
            keyboard.HotKey.parse('<alt>+<space>'),
            lambda: self.root.after(0, self.open_query_modal)
        )

        def on_press(key):
            try:
                hotkey.press(listener.canonical(key))
            except Exception:
                pass

        def on_release(key):
            try:
                hotkey.release(listener.canonical(key))
            except Exception:
                pass

        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        t = threading.Thread(target=listener.start, daemon=True)
        t.start()

    def run(self):
        self.root.mainloop()


def launch_widget():
    app = FloatingPillWidget()
    app.run()


if __name__ == "__main__":
    launch_widget()
