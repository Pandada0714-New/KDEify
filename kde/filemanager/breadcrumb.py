"""
面包屑导航 - Dolphin 风格的地址栏。
"""
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QCompleter,
)
from PySide6.QtCore import Qt, QDir
from PySide6.QtGui import QIcon


class BreadcrumbBar(QWidget):
    """面包屑导航栏"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("BreadcrumbBar")
        self._path = QDir.homePath()
        self._segments = []  # [(name, path), ...]
        self.path_changed = None  # 外部回调

        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(0)

        # 后退/前进/向上按钮
        self.btn_back = QPushButton("◀", self)
        self.btn_back.setFixedSize(28, 28)
        self.btn_back.setEnabled(False)
        self.btn_back.clicked.connect(self._on_back)
        layout.addWidget(self.btn_back)

        self.btn_forward = QPushButton("▶", self)
        self.btn_forward.setFixedSize(28, 28)
        self.btn_forward.setEnabled(False)
        layout.addWidget(self.btn_forward)

        self.btn_up = QPushButton("▲", self)
        self.btn_up.setFixedSize(28, 28)
        self.btn_up.clicked.connect(self._on_up)
        layout.addWidget(self.btn_up)

        # 面包屑容器
        self.crumbs_widget = QWidget(self)
        self.crumbs_layout = QHBoxLayout(self.crumbs_widget)
        self.crumbs_layout.setContentsMargins(0, 0, 0, 0)
        self.crumbs_layout.setSpacing(2)
        layout.addWidget(self.crumbs_widget)

        layout.addStretch()

        # 路径输入框
        self.path_edit = QLineEdit(self)
        self.path_edit.setPlaceholderText("输入路径...")
        self.path_edit.returnPressed.connect(self._on_path_edit)
        layout.addWidget(self.path_edit)

        # 搜索按钮
        self.btn_search = QPushButton("🔍", self)
        self.btn_search.setFixedSize(28, 28)
        layout.addWidget(self.btn_search)

        self.set_path(self._path)

    def set_path(self, path: str):
        self._path = path
        self.path_edit.setText(path)
        self._rebuild_crumbs()

        # 更新向上按钮
        parent = QDir(path).absolutePath()
        self.btn_up.setEnabled(parent != "/" and len(path) > 1)

    def get_path(self) -> str:
        return self._path

    def _rebuild_crumbs(self):
        """重建面包屑按钮"""
        while self.crumbs_layout.count():
            item = self.crumbs_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        path = self._path
        if not path:
            return

        # 分割路径
        if path == "/":
            segments = [("/", "/")]
        else:
            parts = path.split("/")
            segments = []
            current = ""
            for part in parts:
                if not part:
                    continue
                current = f"{current}/{part}"
                segments.append((part, current))
            # 加上根
            if path.startswith("/"):
                segments.insert(0, ("/", "/"))

        for name, seg_path in segments:
            btn = QPushButton(name, self)
            btn.setFlat(True)
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: none;
                    padding: 2px 6px;
                    border-radius: 3px;
                    color: #232629;
                }
                QPushButton:hover {
                    background-color: #3daee9;
                    color: #ffffff;
                }
            """)
            btn.clicked.connect(lambda checked, p=seg_path: self._on_crumb_clicked(p))
            self.crumbs_layout.addWidget(btn)

            # 分隔符
            if seg_path != segments[-1][1]:
                sep = QLabel(" › ", self)
                sep.setStyleSheet("color: #bdc3c7;")
                self.crumbs_layout.addWidget(sep)

        self.crumbs_layout.addStretch()

    def _on_crumb_clicked(self, path: str):
        self.set_path(path)
        if self.path_changed:
            self.path_changed(path)

    def _on_back(self):
        pass  # 由外部实现历史

    def _on_forward(self):
        pass

    def _on_up(self):
        parent = QDir(self._path).absolutePath()
        # 获取父目录
        qdir = QDir(self._path)
        if qdir.cdUp():
            parent = qdir.absolutePath()
            self.set_path(parent)
            if self.path_changed:
                self.path_changed(parent)

    def _on_path_edit(self):
        path = self.path_edit.text().strip()
        if path and QDir(path).exists():
            self.set_path(path)
            if self.path_changed:
                self.path_changed(path)
