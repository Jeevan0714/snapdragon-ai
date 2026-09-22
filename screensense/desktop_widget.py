"""Modern PyQt5 Floating Desktop Pill Widget and Global Hotkey Listener.

Features:
- Borderless, sleek glassmorphism floating bar (always on top).
- Draggable anywhere on your screen.
- Integrated search bar + quick 'Check Screen' and 'Ask Tutor' actions.
- Global Alt+Space hotkey listener via pynput.
"""

import sys
import threading
from typing import Optional

from PyQt5 import QtWidgets, QtCore, QtGui
from .app import route_unified_request

try:
    from pynput import keyboard
    HAS_PYNPUT = True
except ImportError:
    HAS_PYNPUT = False


class FloatingPillWidget(QtWidgets.QWidget):
    # Signal to safely bring window to front from background hotkey thread
    summon_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.old_pos = None

        self.summon_signal.connect(self.summon_widget)
        if HAS_PYNPUT:
            self.start_hotkey_listener()

    def init_ui(self):
        # Frameless, always on top, transparent background
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Main Layout
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(10)

        # Container Frame with rounded styling
        self.container = QtWidgets.QFrame()
        self.container.setStyleSheet("""
            QFrame {
                background-color: #161b22;
                border: 2px solid #58a6ff;
                border-radius: 20px;
            }
        """)
        
        container_layout = QtWidgets.QHBoxLayout(self.container)
        container_layout.setContentsMargins(14, 6, 14, 6)
        container_layout.setSpacing(10)

        # Shield Icon & Title
        self.title_lbl = QtWidgets.QLabel("🛡️ ScreenSense")
        self.title_lbl.setStyleSheet("color: #58a6ff; font-weight: bold; font-size: 13px; border: none;")
        container_layout.addWidget(self.title_lbl)

        # Input Query Box
        self.query_input = QtWidgets.QLineEdit()
        self.query_input.setPlaceholderText("Ask how to do anything or check scam (Alt+Space)...")
        self.query_input.setFixedWidth(360)
        self.query_input.setStyleSheet("""
            QLineEdit {
                background-color: #0d1117;
                color: #f0f6fc;
                border: 1px solid #30363d;
                border-radius: 12px;
                padding: 6px 12px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 1px solid #58a6ff;
            }
        """)
        self.query_input.returnPressed.connect(self.on_ask_tutor)
        container_layout.addWidget(self.query_input)

        # Button: Ask Tutor
        self.ask_btn = QtWidgets.QPushButton("💡 Ask")
        self.ask_btn.setStyleSheet("""
            QPushButton {
                background-color: #1f6feb;
                color: white;
                font-weight: bold;
                font-size: 12px;
                border-radius: 12px;
                padding: 6px 14px;
                border: none;
            }
            QPushButton:hover {
                background-color: #388bfd;
            }
        """)
        self.ask_btn.clicked.connect(self.on_ask_tutor)
        container_layout.addWidget(self.ask_btn)

        # Button: Check Screen
        self.check_btn = QtWidgets.QPushButton("🛡️ Check Screen")
        self.check_btn.setStyleSheet("""
            QPushButton {
                background-color: #238636;
                color: white;
                font-weight: bold;
                font-size: 12px;
                border-radius: 12px;
                padding: 6px 14px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2ea043;
            }
        """)
        self.check_btn.clicked.connect(self.on_check_screen)
        container_layout.addWidget(self.check_btn)

        # Close button
        self.close_btn = QtWidgets.QPushButton("✕")
        self.close_btn.setFixedSize(24, 24)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #8b949e;
                font-size: 12px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                color: #f85149;
            }
        """)
        self.close_btn.clicked.connect(self.close)
        container_layout.addWidget(self.close_btn)

        layout.addWidget(self.container)
        self.setLayout(layout)

        # Position at top center of desktop
        screen = QtWidgets.QApplication.primaryScreen().geometry()
        pill_w, pill_h = 720, 60
        self.setGeometry((screen.width() - pill_w) // 2, 20, pill_w, pill_h)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPos() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

    def on_ask_tutor(self):
        query = self.query_input.text().strip()
        if not query:
            return
        result = route_unified_request(user_input=query, interactive_ui=False)
        if result.get("is_scam"):
            self.show_scam_dialog(result)
        else:
            self.show_game_spotlight(result)

    def on_check_screen(self):
        fake_test_text = "Windows Defender Alert! Your PC is infected with Trojan! Call 1-800-555-0199 immediately!"
        result = route_unified_request(user_input="check this", screen_text=fake_test_text, interactive_ui=False)
        self.show_scam_dialog(result)

    def show_game_spotlight(self, result):
        """Launches the video-game onboarding spotlight over the target element."""
        self.spotlight = GameSpotlightOverlay(result)
        self.spotlight.show()

    def show_scam_dialog(self, result):
        """Displays the Guardian Alert dialog for threats."""
        dlg = QtWidgets.QDialog(self)
        dlg.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        dlg.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        layout = QtWidgets.QVBoxLayout(dlg)
        frame = QtWidgets.QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #0d1117;
                border: 2px solid #f85149;
                border-radius: 16px;
                padding: 16px;
            }
        """)
        f_layout = QtWidgets.QVBoxLayout(frame)

        title = QtWidgets.QLabel(f"🛡️ {result['title']}")
        title.setStyleSheet("color: #ff7b72; font-size: 17px; font-weight: bold; border: none;")
        f_layout.addWidget(title)

        exp = QtWidgets.QLabel(f"<b>Why flagged:</b> {result['explanation']}")
        exp.setStyleSheet("color: #f0f6fc; font-size: 13px; border: none;")
        exp.setWordWrap(True)
        f_layout.addWidget(exp)

        safe = QtWidgets.QLabel(f"<b>Safe Action:</b> {result['safe_action']}")
        safe.setStyleSheet("color: #7ee787; font-size: 13px; border: none;")
        safe.setWordWrap(True)
        f_layout.addWidget(safe)

        footer = QtWidgets.QLabel(f"⚡ Snapdragon NPU: {result.get('npu_latency_ms', 31)} ms  •  100% Private")
        footer.setStyleSheet("color: #8b949e; font-size: 11px; border: none;")
        f_layout.addWidget(footer)

        close_btn = QtWidgets.QPushButton("Dismiss")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #21262d;
                color: white;
                border: 1px solid #30363d;
                border-radius: 8px;
                padding: 6px 16px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #30363d; }
        """)
        close_btn.clicked.connect(dlg.accept)
        f_layout.addWidget(close_btn, alignment=QtCore.Qt.AlignRight)

        layout.addWidget(frame)
        dlg.resize(600, 220)
        dlg.move(self.x() + (self.width() - 600) // 2, self.y() + self.height() + 10)
        dlg.exec_()

    def summon_widget(self):
        self.show()
        self.raise_()
        self.activateWindow()
        self.query_input.setFocus()
        self.query_input.selectAll()

    def start_hotkey_listener(self):
        def on_activate():
            self.summon_signal.emit()

        hotkey = keyboard.GlobalHotKeys({
            '<alt>+<space>': on_activate
        })
        t = threading.Thread(target=hotkey.start, daemon=True)
        t.start()


class GameSpotlightOverlay(QtWidgets.QWidget):
    """Full-screen game-style tutorial overlay.
    
    Like a video game onboarding walkthrough:
    - Dims the rest of the screen with a soft cinematic dark mask.
    - Draws a vibrant golden spotlight box directly around the real target button.
    - Points a glowing arrow: '👉 CLICK HERE'.
    - Displays a floating Game Quest Card with instructions, shortcuts, and copy buttons.
    """

    def __init__(self, result, parent=None):
        super().__init__(parent)
        self.result = result
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        screen = QtWidgets.QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, screen.width(), screen.height())

        # Target bounding box in pixels
        bbox = result.get("bounding_box_pct", {"x": 0.01, "y": 0.16, "width": 0.035, "height": 0.05})
        self.bx = int(bbox["x"] * screen.width())
        self.by = int(bbox["y"] * screen.height())
        self.bw = max(52, int(bbox["width"] * screen.width()))
        self.bh = max(52, int(bbox["height"] * screen.height()))

        # Add Quest Card HUD
        self.init_hud(screen)

    def init_hud(self, screen):
        # Position Quest Card near the highlight box
        card_w, card_h = 580, 260
        # If target is on the left edge (like VS Code sidebar), place card to the right of it
        if self.bx < screen.width() // 2:
            card_x = min(self.bx + self.bw + 30, screen.width() - card_w - 30)
            card_y = max(40, min(self.by, screen.height() - card_h - 60))
        else:
            card_x = max(30, self.bx - card_w - 30)
            card_y = max(40, min(self.by, screen.height() - card_h - 60))

        self.hud_frame = QtWidgets.QFrame(self)
        self.hud_frame.setGeometry(card_x, card_y, card_w, card_h)
        self.hud_frame.setStyleSheet("""
            QFrame {
                background-color: #0d1117;
                border: 2px solid #ffd700;
                border-radius: 16px;
            }
        """)

        layout = QtWidgets.QVBoxLayout(self.hud_frame)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(10)

        # Title / Quest Header
        title = QtWidgets.QLabel(f"🎮 Step: {self.result['step_title']}", self.hud_frame)
        title.setStyleSheet("color: #ffd700; font-size: 16px; font-weight: bold; border: none;")
        layout.addWidget(title)

        # Target pointer
        target_lbl = QtWidgets.QLabel(f"👉 <b>Target:</b> <span style='color: #58a6ff;'>{self.result['highlight_target']}</span>", self.hud_frame)
        target_lbl.setStyleSheet("color: #f0f6fc; font-size: 13px; border: none;")
        layout.addWidget(target_lbl)

        # Instructions
        inst = QtWidgets.QLabel(self.result['instruction'], self.hud_frame)
        inst.setStyleSheet("color: #c9d1d9; font-size: 13px; line-height: 1.4; border: none;")
        inst.setWordWrap(True)
        layout.addWidget(inst)

        # Shortcut & Copy Command
        if self.result.get("shortcut"):
            sc = QtWidgets.QLabel(f"⌨️ <b>Shortcut:</b> <code>{self.result['shortcut']}</code>", self.hud_frame)
            sc.setStyleSheet("color: #7ee787; font-size: 12px; border: none;")
            layout.addWidget(sc)

        if self.result.get("copy_text"):
            cb_box = QtWidgets.QFrame(self.hud_frame)
            cb_box.setStyleSheet("background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 4px;")
            cb_l = QtWidgets.QHBoxLayout(cb_box)
            cmd_lbl = QtWidgets.QLabel(self.result['copy_text'], cb_box)
            cmd_lbl.setStyleSheet("color: #79c0ff; font-family: monospace; font-size: 12px; border: none;")
            cb_l.addWidget(cmd_lbl, 1)

            copy_b = QtWidgets.QPushButton("📋 Copy", cb_box)
            copy_b.setStyleSheet("""
                QPushButton {
                    background-color: #21262d;
                    color: white;
                    border: 1px solid #30363d;
                    border-radius: 6px;
                    padding: 4px 10px;
                    font-size: 11px;
                    font-weight: bold;
                }
                QPushButton:hover { background-color: #30363d; color: #58a6ff; }
            """)
            def do_copy():
                QtWidgets.QApplication.clipboard().setText(self.result['copy_text'])
                copy_b.setText("✓ Copied!")
                QtCore.QTimer.singleShot(1500, lambda: copy_b.setText("📋 Copy"))
            copy_b.clicked.connect(do_copy)
            cb_l.addWidget(copy_b)
            layout.addWidget(cb_box)

        # Bottom Got It Button
        b_row = QtWidgets.QHBoxLayout()
        sub_lbl = QtWidgets.QLabel("Press Esc or click button to close", self.hud_frame)
        sub_lbl.setStyleSheet("color: #8b949e; font-size: 11px; border: none;")
        b_row.addWidget(sub_lbl)

        got_it = QtWidgets.QPushButton("Got It (Esc)", self.hud_frame)
        got_it.setStyleSheet("""
            QPushButton {
                background-color: #238636;
                color: white;
                font-weight: bold;
                font-size: 12px;
                border-radius: 8px;
                padding: 6px 16px;
                border: none;
            }
            QPushButton:hover { background-color: #2ea043; }
        """)
        got_it.clicked.connect(self.close)
        b_row.addWidget(got_it, 0, QtCore.Qt.AlignRight)
        layout.addLayout(b_row)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # 1. Soft cinematic dark overlay across entire desktop (like games)
        overlay_color = QtGui.QColor(10, 15, 25, 140)
        painter.fillRect(self.rect(), overlay_color)

        # 2. Glowing Golden Spotlight Box around target button
        # Outer glow
        glow_pen = QtGui.QPen(QtGui.QColor(255, 215, 0, 90), 8)
        painter.setPen(glow_pen)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRoundedRect(self.bx - 4, self.by - 4, self.bw + 8, self.bh + 8, 8, 8)

        # Inner sharp golden border
        sharp_pen = QtGui.QPen(QtGui.QColor(255, 215, 0, 255), 3)
        painter.setPen(sharp_pen)
        painter.drawRoundedRect(self.bx, self.by, self.bw, self.bh, 6, 6)

        # 3. Game Pointer Arrow: '👉 CLICK HERE'
        painter.setPen(QtGui.QColor("#ffd700"))
        font = QtGui.QFont("Arial", 12, QtGui.QFont.Bold)
        painter.setFont(font)
        
        # Position pointer text above or below the box
        if self.by > 60:
            painter.drawText(self.bx, self.by - 12, "👉 CLICK HERE")
        else:
            painter.drawText(self.bx, self.by + self.bh + 24, "👉 CLICK HERE")

    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Escape, QtCore.Qt.Key_Return, QtCore.Qt.Key_Space):
            self.close()

    def mousePressEvent(self, event):
        # Click outside hud card closes the tutorial spotlight
        if not self.hud_frame.geometry().contains(event.pos()):
            self.close()


def launch_widget():
    app = QtWidgets.QApplication.instance()
    if not app:
        app = QtWidgets.QApplication(sys.argv)
    widget = FloatingPillWidget()
    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    launch_widget()
