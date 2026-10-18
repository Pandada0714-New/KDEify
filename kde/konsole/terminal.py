"""
Konsole 风格终端 - 基于 QProcess + QTextEdit 的简单终端模拟器。
支持 ANSI 颜色、基本交互、多标签页。
"""
import os
import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QTabWidget, QPushButton, QLabel, QComboBox,
    QFileDialog, QMessageBox, QSplitter, QMenu,
)
from PySide6.QtCore import QProcess, Qt, QByteArray
from PySide6.QtGui import QTextCursor, QColor, QFont, QTextCharFormat, QAction


class TerminalWidget(QTextEdit):
    """终端显示控件 - 解析 ANSI 颜色"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TerminalWidget")
        self.setReadOnly(True)
        self.setUndoRedoEnabled(False)
        self.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)

        # 终端字体
        font = QFont("Cascadia Mono", 10)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.setFont(font)

        # 颜色映射 (ANSI -> QColor)
        self._ansi_colors = {
            30: QColor("#232629"),  # black
            31: QColor("#da4453"),  # red
            32: QColor("#27ae60"),  # green
            33: QColor("#f67400"),  # yellow
            34: QColor("#2980b9"),  # blue
            35: QColor("#8e44ad"),  # magenta
            36: QColor("#16a085"),  # cyan
            37: QColor("#eff0f1"),  # white
            90: QColor("#6d6d6d"),  # bright black
            91: QColor("#da4453"),  # bright red
            92: QColor("#2ecc71"),  # bright green
            93: QColor("#f39c12"),  # bright yellow
            94: QColor("#3498db"),  # bright blue
            95: QColor("#9b59b6"),  # bright magenta
            96: QColor("#1abc9c"),  # bright cyan
            97: QColor("#ffffff"),  # bright white
        }

        self._current_format = QTextCharFormat()
        self._current_format.setFont(font)
        self._current_format.setForeground(QColor("#eff0f1"))
        self._current_format.setBackground(QColor("#232629"))

        self.setStyleSheet("""
            QTextEdit {
                background-color: #232629;
                color: #eff0f1;
                border: none;
                padding: 4px;
            }
        """)

        # 进程
        self._process = None
        self._shell = None
        self._init_shell()

    def _init_shell(self):
        """初始化 shell 进程"""
        if sys.platform == "win32":
            # Windows: 用 cmd.exe 或 PowerShell
            shell = os.environ.get("KDEIFY_SHELL", "cmd.exe")
            self._shell = shell
            self._process = QProcess(self)
            self._process.setProgram(shell)
            self._process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
            self._process.readyReadStandardOutput.connect(self._read_output)
            self._process.finished.connect(self._on_finished)
            self._process.start()
        else:
            # Linux/Mac: 用 bash 或 zsh
            shell = os.environ.get("SHELL", "/bin/bash")
            self._shell = shell
            self._process = QProcess(self)
            self._process.setProgram(shell)
            self._process.setArguments(["-i"])
            self._process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
            self._process.readyReadStandardOutput.connect(self._read_output)
            self._process.finished.connect(self._on_finished)
            self._process.start()

    def _read_output(self):
        data = self._process.readAllStandardOutput()
        text = bytes(data).decode("utf-8", errors="replace")
        self._append_text(text)

    def _append_text(self, text: str):
        """追加文本，解析 ANSI 转义序列"""
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)

        i = 0
        while i < len(text):
            if text[i] == '\x1b' and i + 1 < len(text) and text[i + 1] == '[':
                # ANSI 转义序列
                j = i + 2
                while j < len(text) and text[j] not in 'mABCDEFGHJKSTfhl':
                    j += 1
                if j < len(text):
                    code = text[j]
                    params = text[i + 2:j]
                    self._handle_ansi(code, params)
                    i = j + 1
                    continue
            if text[i] == '\r':
                # 回车：光标移到行首
                cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
                i += 1
                continue
            if text[i] == '\n':
                cursor.insertBlock()
                i += 1
                continue
            if text[i] == '\x08':
                # 退格
                cursor.deletePreviousChar()
                i += 1
                continue
            if text[i] == '\x07':
                # BEL（响铃），忽略
                i += 1
                continue
            # 普通字符
            cursor.insertText(text[i], self._current_format)
            i += 1

        self.setTextCursor(cursor)
        self.ensureCursorVisible()

    def _handle_ansi(self, code: str, params: str):
        """处理 ANSI 转义序列"""
        if code == 'm':
            if not params or params == '0':
                # 重置
                self._current_format = QTextCharFormat()
                self._current_format.setFont(self.font())
                self._current_format.setForeground(QColor("#eff0f1"))
                self._current_format.setBackground(QColor("#232629"))
            else:
                parts = params.split(';')
                for p in parts:
                    try:
                        num = int(p)
                        if num in self._ansi_colors:
                            self._current_format.setForeground(self._ansi_colors[num])
                        elif num == 1:
                            self._current_format.setFontWeight(QFont.Weight.Bold)
                        elif num == 22:
                            self._current_format.setFontWeight(QFont.Weight.Normal)
                    except ValueError:
                        pass
        elif code == 'H' or code == 'f':
            # 光标定位，简单处理：忽略
            pass
        elif code == 'J':
            # 清屏
            if params == '2':
                self.clear()
        elif code == 'K':
            # 清除到行尾
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.EndOfLine, QTextCursor.MoveMode.KeepAnchor)
            cursor.removeSelectedText()

    def send_command(self, cmd: str):
        """发送命令到 shell"""
        if self._process and self._process.state() == QProcess.ProcessState.Running:
            self._process.write(QByteArray((cmd + "\n").encode("utf-8")))

    def keyPressEvent(self, event):
        """键盘输入转发到 shell"""
        if self._process and self._process.state() == QProcess.ProcessState.Running:
            key = event.key()
            text = event.text()

            if key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
                self._process.write(b"\r\n")
            elif key == Qt.Key.Key_Backspace:
                self._process.write(b"\x7f")
            elif key == Qt.Key.Key_Tab:
                self._process.write(b"\t")
            elif key == Qt.Key.Key_Up:
                self._process.write(b"\x1b[A")
            elif key == Qt.Key.Key_Down:
                self._process.write(b"\x1b[B")
            elif key == Qt.Key.Key_Right:
                self._process.write(b"\x1b[C")
            elif key == Qt.Key.Key_Left:
                self._process.write(b"\x1b[D")
            elif key == Qt.Key.Key_C and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                self._process.write(b"\x03")
            elif key == Qt.Key.Key_D and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                self._process.write(b"\x04")
            elif key == Qt.Key.Key_Z and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                self._process.write(b"\x1a")
            elif text:
                self._process.write(text.encode("utf-8"))
        else:
            super().keyPressEvent(event)

    def _on_finished(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText("\n[进程已退出]\n")
        self.setTextCursor(cursor)

    def closeEvent(self, event):
        if self._process:
            self._process.terminate()
            if not self._process.waitForFinished(1000):
                self._process.kill()
        super().closeEvent(event)
