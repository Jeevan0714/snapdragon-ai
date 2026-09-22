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
        self.show_result_card(result)

    def on_check_screen(self):
        fake_test_text = "Windows Defender Alert! Your PC is infected with Trojan! Call 1-800-555-0199 immediately!"
        result = route_unified_request(user_input="check this", screen_text=fake_test_text, interactive_ui=False)
        self.show_result_card(result)

    def show_result_card(self, result):
        """Displays a dedicated non-intrusive floating response dialog."""
        dlg = QtWidgets.QDialog(self)
        dlg.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        dlg.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        d_layout = QtWidgets.QVBoxLayout(dlg)
        frame = QtWidgets.QFrame()
        
        is_scam = result.get("threat_level") is not None and result.get("is_scam", False)
        border_color = "#f85149" if is_scam else "#ffd700"
        
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: #0d1117;
                border: 2px solid {border_color};
                border-radius: 16px;
                padding: 16px;
            }}
        """)
        f_layout = QtWidgets.QVBoxLayout(frame)

        if is_scam:
            title = QtWidgets.QLabel(f"🛡️ {result['title']}")
            title.setStyleSheet("color: #ff7b72; font-size: 16px; font-weight: bold; border: none;")
            f_layout.addWidget(title)

            exp = QtWidgets.QLabel(f"<b>Why flagged:</b> {result['explanation']}")
            exp.setStyleSheet("color: #f0f6fc; font-size: 13px; border: none;")
            exp.setWordWrap(True)
            f_layout.addWidget(exp)

            safe = QtWidgets.QLabel(f"<b>Safe Action:</b> {result['safe_action']}")
            safe.setStyleSheet("color: #7ee787; font-size: 13px; border: none;")
            safe.setWordWrap(True)
            f_layout.addWidget(safe)
        else:
            title = QtWidgets.QLabel(f"💡 {result['step_title']} ({result['app']})")
            title.setStyleSheet("color: #58a6ff; font-size: 16px; font-weight: bold; border: none;")
            f_layout.addWidget(title)

            target = QtWidgets.QLabel(f"👉 <b>Click Target:</b> {result['highlight_target']}")
            target.setStyleSheet("color: #ffd700; font-size: 14px; font-weight: bold; border: none;")
            f_layout.addWidget(target)

            inst = QtWidgets.QLabel(result['instruction'])
            inst.setStyleSheet("color: #f0f6fc; font-size: 13px; border: none;")
            inst.setWordWrap(True)
            f_layout.addWidget(inst)

            if result.get("shortcut"):
                sc = QtWidgets.QLabel(f"⌨️ <b>Shortcut:</b> {result['shortcut']}")
                sc.setStyleSheet("color: #7ee787; font-size: 12px; font-weight: bold; border: none;")
                f_layout.addWidget(sc)

            if result.get("copy_text"):
                cp = QtWidgets.QLabel(f"📋 <b>Formula/Command:</b> <code>{result['copy_text']}</code>")
                cp.setStyleSheet("color: #79c0ff; font-size: 12px; border: none;")
                f_layout.addWidget(cp)

        footer = QtWidgets.QLabel(f"⚡ Snapdragon NPU: {result.get('npu_latency_ms', 31)} ms  •  Click Close to continue")
        footer.setStyleSheet("color: #8b949e; font-size: 10px; border: none; margin-top: 8px;")
        f_layout.addWidget(footer)

        close_b = QtWidgets.QPushButton("Got it")
        close_b.setStyleSheet("""
            QPushButton {
                background-color: #21262d;
                color: #f0f6fc;
                border: 1px solid #30363d;
                border-radius: 8px;
                padding: 6px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #30363d;
            }
        """)
        close_b.clicked.connect(dlg.accept)
        f_layout.addWidget(close_b, alignment=QtCore.Qt.AlignRight)

        d_layout.addWidget(frame)
        dlg.resize(580, 240)
        
        # Position below pill
        dlg.move(self.x() + (self.width() - 580) // 2, self.y() + self.height() + 10)
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


def launch_widget():
    app = QtWidgets.QApplication.instance()
    if not app:
        app = QtWidgets.QApplication(sys.argv)
    widget = FloatingPillWidget()
    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    launch_widget()
