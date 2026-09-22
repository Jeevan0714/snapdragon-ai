"""Accessible Desktop Overlay UI for ScreenSense Guardian.

Features:
- High-contrast, senior-friendly typography and generous padding.
- Golden pulsing highlight rectangle over target UI elements.
- Soft protective shield banner for Guardian scam interception.
- Zero-fuss cross-platform runtime using Python's built-in Tkinter.
"""

import sys
import time
from typing import Dict, Any, Optional

try:
    import tkinter as tk
    from tkinter import ttk
    HAS_TK = True
except ImportError:
    HAS_TK = False


class ScreenOverlay:
    """Manages transparent desktop highlight boxes and calm guidance cards."""

    def __init__(self, headless: bool = False):
        self.headless = headless or not HAS_TK
        self.root = None

    def display_guide(self, guide_data: Dict[str, Any], duration_sec: int = 6):
        """Renders the golden highlight box and patient instruction card."""
        if self.headless:
            self._print_guide_terminal(guide_data)
            return

        try:
            self.root = tk.Tk()
            self.root.title("ScreenSense Guide Overlay")
            
            # Fullscreen transparent window attributes
            screen_w = self.root.winfo_screenwidth()
            screen_h = self.root.winfo_screenheight()
            self.root.geometry(f"{screen_w}x{screen_h}+0+0")
            
            # Cross-platform window configuration
            self.root.attributes("-topmost", True)
            try:
                # Windows & Linux window transparency
                self.root.attributes("-alpha", 0.94)
            except Exception:
                pass

            # Main canvas
            canvas = tk.Canvas(self.root, bg="#0d1117", highlightthickness=0)
            canvas.pack(fill=tk.BOTH, expand=True)

            # Draw target bounding box (Golden Highlight)
            bbox = guide_data.get("bounding_box_pct", {"x": 0.25, "y": 0.1, "width": 0.1, "height": 0.05})
            bx = int(bbox["x"] * screen_w)
            by = int(bbox["y"] * screen_h)
            bw = int(bbox["width"] * screen_w)
            bh = int(bbox["height"] * screen_h)

            # Outer glow and border
            canvas.create_rectangle(bx - 4, by - 4, bx + bw + 4, by + bh + 4, outline="#ffd700", width=4)
            canvas.create_rectangle(bx, by, bx + bw, by + bh, outline="#ffffff", width=2)
            
            # Pointer label pointing to the button
            canvas.create_line(bx + bw // 2, by + bh + 4, bx + bw // 2, by + bh + 30, fill="#ffd700", width=3)
            canvas.create_text(bx + bw // 2, by + bh + 45, text=f"👉 Click Here: {guide_data['highlight_target']}",
                               fill="#ffd700", font=("Arial", 12, "bold"))

            # Bottom Guidance Card (Patient Tutor)
            card_w, card_h = 760, 200
            cx = (screen_w - card_w) // 2
            cy = screen_h - card_h - 60

            canvas.create_rectangle(cx, cy, cx + card_w, cy + card_h, fill="#161b22", outline="#30363d", width=2)
            
            # Card Title & App Badge
            canvas.create_text(cx + 30, cy + 30, text=f"💡 {guide_data['step_title']}",
                               fill="#58a6ff", font=("Arial", 16, "bold"), anchor="w")
            canvas.create_text(cx + card_w - 30, cy + 30, text=f"[{guide_data['app']}]",
                               fill="#8b949e", font=("Arial", 11, "bold"), anchor="e")

            # Instruction Body
            canvas.create_text(cx + 30, cy + 75, text=guide_data['instruction'],
                               fill="#f0f6fc", font=("Arial", 13), anchor="w", width=card_w - 60)

            # Shortcut & Actions
            extra_info = ""
            if guide_data.get("shortcut"):
                extra_info += f"⌨️ Keyboard Shortcut: {guide_data['shortcut']}    "
            if guide_data.get("copy_text"):
                extra_info += f"📋 Formula/Text: {guide_data['copy_text']}"
            
            canvas.create_text(cx + 30, cy + 130, text=extra_info,
                               fill="#7ee787", font=("Arial", 12, "bold"), anchor="w")

            canvas.create_text(cx + card_w - 30, cy + 170, text=f"⚡ Snapdragon NPU: {guide_data.get('npu_latency_ms', 42)}ms  •  Press any key or click to dismiss",
                               fill="#8b949e", font=("Arial", 10), anchor="e")

            # Dismiss triggers
            self.root.bind("<Key>", lambda e: self.root.destroy())
            self.root.bind("<Button-1>", lambda e: self.root.destroy())
            self.root.after(duration_sec * 1000, lambda: self.root.destroy() if self.root else None)
            
            self.root.mainloop()
        except Exception as e:
            print(f"[Overlay] Window rendering skipped ({e}). Showing terminal output:")
            self._print_guide_terminal(guide_data)

    def display_guardian_alert(self, scam_data: Dict[str, Any], duration_sec: int = 8):
        """Renders the calm, protective Guardian Shield alert."""
        if self.headless:
            self._print_scam_terminal(scam_data)
            return

        try:
            self.root = tk.Tk()
            self.root.title("ScreenSense Guardian Shield")
            screen_w = self.root.winfo_screenwidth()
            screen_h = self.root.winfo_screenheight()
            self.root.geometry(f"{screen_w}x{screen_h}+0+0")
            
            self.root.attributes("-topmost", True)
            try:
                self.root.attributes("-alpha", 0.96)
            except Exception:
                pass

            canvas = tk.Canvas(self.root, bg="#0d1117", highlightthickness=0)
            canvas.pack(fill=tk.BOTH, expand=True)

            card_w, card_h = 800, 320
            cx = (screen_w - card_w) // 2
            cy = (screen_h - card_h) // 2

            # Soft warning banner border
            canvas.create_rectangle(cx, cy, cx + card_w, cy + card_h, fill="#1c1212", outline="#f85149", width=3)
            
            # Header
            canvas.create_text(cx + 40, cy + 40, text=f"🛡️ {scam_data['title']}",
                               fill="#ff7b72", font=("Arial", 18, "bold"), anchor="w")
            
            # Calm Explanation
            canvas.create_text(cx + 40, cy + 90, text="Why ScreenSense Guardian flagged this:",
                               fill="#8b949e", font=("Arial", 12, "bold"), anchor="w")
            canvas.create_text(cx + 40, cy + 125, text=scam_data['explanation'],
                               fill="#f0f6fc", font=("Arial", 13), anchor="w", width=card_w - 80)

            # Recommended Safe Action
            canvas.create_text(cx + 40, cy + 180, text="Recommended Safe Action:",
                               fill="#7ee787", font=("Arial", 12, "bold"), anchor="w")
            canvas.create_text(cx + 40, cy + 215, text=scam_data['safe_action'],
                               fill="#e6edf3", font=("Arial", 13), anchor="w", width=card_w - 80)

            canvas.create_text(cx + 40, cy + 280, text=f"🔒 {scam_data.get('privacy', '100% Private on Hexagon NPU')}  •  Click anywhere or press Esc to dismiss",
                               fill="#8b949e", font=("Arial", 10), anchor="w")

            self.root.bind("<Key>", lambda e: self.root.destroy())
            self.root.bind("<Button-1>", lambda e: self.root.destroy())
            self.root.after(duration_sec * 1000, lambda: self.root.destroy() if self.root else None)

            self.root.mainloop()
        except Exception as e:
            print(f"[Overlay] Window rendering skipped ({e}). Showing terminal output:")
            self._print_scam_terminal(scam_data)

    def _print_guide_terminal(self, guide_data: Dict[str, Any]):
        print("\n" + "=" * 70)
        print(f"💡 [GUIDE MODE] {guide_data['step_title']} ({guide_data['app']})")
        print("-" * 70)
        print(f"Instruction : {guide_data['instruction']}")
        print(f"Target      : {guide_data['highlight_target']}")
        if guide_data.get("shortcut"):
            print(f"Shortcut    : {guide_data['shortcut']}")
        if guide_data.get("copy_text"):
            print(f"Copy Box    : {guide_data['copy_text']}")
        print(f"Hardware    : Snapdragon Hexagon NPU ({guide_data.get('npu_latency_ms', 42)} ms)")
        print("=" * 70 + "\n")

    def _print_scam_terminal(self, scam_data: Dict[str, Any]):
        print("\n" + "!" * 70)
        print(f"🛡️ [GUARDIAN ALERT] {scam_data['title']}")
        print("-" * 70)
        print(f"Why Flagged : {scam_data['explanation']}")
        print(f"Safe Action : {scam_data['safe_action']}")
        print(f"Privacy     : {scam_data.get('privacy', 'Processed locally on Snapdragon NPU')}")
        print("!" * 70 + "\n")


overlay = ScreenOverlay()
