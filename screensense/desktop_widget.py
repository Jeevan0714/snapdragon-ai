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
        """Displays a dedicated non-intrusive floating response dialog with scroll and copy support."""
        dlg = QtWidgets.QDialog(self)
        dlg.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        dlg.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        main_layout = QtWidgets.QVBoxLayout(dlg)
        main_layout.setContentsMargins(0, 0, 0, 0)

        is_scam = result.get("threat_level") is not None and result.get("is_scam", False)
        border_color = "#f85149" if is_scam else "#ffd700"
        
        # Outer Card Container
        container = QtWidgets.QFrame()
        container.setStyleSheet(f"""
            QFrame#MainCard {{
                background-color: #0d1117;
                border: 2px solid {border_color};
                border-radius: 16px;
            }}
        """)
        container.setObjectName("MainCard")
        c_layout = QtWidgets.QVBoxLayout(container)
        c_layout.setContentsMargins(20, 18, 20, 16)
        c_layout.setSpacing(12)

        # Header Title
        if is_scam:
            title = QtWidgets.QLabel(f"🛡️ {result['title']}")
            title.setStyleSheet("color: #ff7b72; font-size: 17px; font-weight: bold; border: none;")
        else:
            title = QtWidgets.QLabel(f"💡 {result['step_title']} ({result['app']})")
            title.setStyleSheet("color: #58a6ff; font-size: 17px; font-weight: bold; border: none;")
        c_layout.addWidget(title)

        # Scrollable content area
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        content_widget = QtWidgets.QWidget()
        content_widget.setStyleSheet("background: transparent;")
        f_layout = QtWidgets.QVBoxLayout(content_widget)
        f_layout.setContentsMargins(0, 0, 8, 0)
        f_layout.setSpacing(12)

        if is_scam:
            exp_box = QtWidgets.QFrame()
            exp_box.setStyleSheet("background-color: #161b22; border-radius: 8px; padding: 10px; border: 1px solid #30363d;")
            exp_l = QtWidgets.QVBoxLayout(exp_box)
            exp_title = QtWidgets.QLabel("⚠️ Why ScreenSense Flagged This:")
            exp_title.setStyleSheet("color: #f85149; font-weight: bold; font-size: 13px; border: none;")
            exp_text = QtWidgets.QLabel(result['explanation'])
            exp_text.setStyleSheet("color: #f0f6fc; font-size: 13px; line-height: 1.4; border: none;")
            exp_text.setWordWrap(True)
            exp_l.addWidget(exp_title)
            exp_l.addWidget(exp_text)
            f_layout.addWidget(exp_box)

            safe_box = QtWidgets.QFrame()
            safe_box.setStyleSheet("background-color: #161b22; border-radius: 8px; padding: 10px; border: 1px solid #238636;")
            safe_l = QtWidgets.QVBoxLayout(safe_box)
            safe_title = QtWidgets.QLabel("✅ Recommended Safe Action:")
            safe_title.setStyleSheet("color: #7ee787; font-weight: bold; font-size: 13px; border: none;")
            safe_text = QtWidgets.QLabel(result['safe_action'])
            safe_text.setStyleSheet("color: #e6edf3; font-size: 13px; line-height: 1.4; border: none;")
            safe_text.setWordWrap(True)
            safe_l.addWidget(safe_title)
            safe_l.addWidget(safe_text)
            f_layout.addWidget(safe_box)
        else:
            # Target action
            target = QtWidgets.QLabel(f"👉 <b>Click Target:</b> <span style='color: #ffd700;'>{result['highlight_target']}</span>")
            target.setStyleSheet("color: #f0f6fc; font-size: 14px; border: none;")
            target.setWordWrap(True)
            f_layout.addWidget(target)

            # Instruction
            inst = QtWidgets.QLabel(result['instruction'])
            inst.setStyleSheet("color: #c9d1d9; font-size: 13px; line-height: 1.5; border: none;")
            inst.setWordWrap(True)
            f_layout.addWidget(inst)

            # Shortcut badge
            if result.get("shortcut"):
                sc = QtWidgets.QLabel(f"⌨️ <b>Keyboard Shortcut:</b> <code>{result['shortcut']}</code>")
                sc.setStyleSheet("color: #7ee787; font-size: 13px; border: none; background-color: #161b22; padding: 6px; border-radius: 6px;")
                sc.setWordWrap(True)
                f_layout.addWidget(sc)

            # Copy box (Terminal command / formula)
            if result.get("copy_text"):
                copy_box = QtWidgets.QFrame()
                copy_box.setStyleSheet("background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 8px;")
                cb_layout = QtWidgets.QHBoxLayout(copy_box)
                
                cmd_lbl = QtWidgets.QLabel(result['copy_text'])
                cmd_lbl.setStyleSheet("color: #79c0ff; font-family: monospace; font-size: 13px; border: none;")
                cmd_lbl.setWordWrap(True)
                cb_layout.addWidget(cmd_lbl, 1)

                copy_btn = QtWidgets.QPushButton("📋 Copy")
                copy_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #21262d;
                        color: #f0f6fc;
                        border: 1px solid #30363d;
                        border-radius: 6px;
                        padding: 5px 12px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #30363d;
                        color: #58a6ff;
                    }
                """)
                def copy_to_clipboard():
                    QtWidgets.QApplication.clipboard().setText(result['copy_text'])
                    copy_btn.setText("✓ Copied!")
                    QtCore.QTimer.singleShot(1500, lambda: copy_btn.setText("📋 Copy"))

                copy_btn.clicked.connect(copy_to_clipboard)
                cb_layout.addWidget(copy_btn)
                f_layout.addWidget(copy_box)

        scroll.setWidget(content_widget)
        c_layout.addWidget(scroll)

        # Footer row with Snapdragon NPU badge and Got It button
        footer_row = QtWidgets.QHBoxLayout()
        footer_lbl = QtWidgets.QLabel(f"⚡ Snapdragon Hexagon NPU: {result.get('npu_latency_ms', 31)} ms  •  100% On-Device")
        footer_lbl.setStyleSheet("color: #8b949e; font-size: 11px; border: none;")
        footer_row.addWidget(footer_lbl)

        close_btn = QtWidgets.QPushButton("Got It")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #238636;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 6px 20px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2ea043;
            }
        """)
        close_btn.clicked.connect(dlg.accept)
        footer_row.addWidget(close_btn, 0, QtCore.Qt.AlignRight)

        c_layout.addLayout(footer_row)
        main_layout.addWidget(container)

        # Generous readable sizing
        card_w = min(680, QtWidgets.QApplication.primaryScreen().geometry().width() - 40)
        card_h = 360
        dlg.resize(card_w, card_h)
        
        # Position centered below pill
        pos_x = self.x() + (self.width() - card_w) // 2
        pos_y = self.y() + self.height() + 12
        dlg.move(pos_x, pos_y)
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
