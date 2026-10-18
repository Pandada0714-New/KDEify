"""
侧边栏 - Dolphin 风格的 Places 面板。
包含：常用位置、设备、书签。
"""
from PySide6.QtWidgets import (
    QListWidget, QListWidgetItem, QLabel, QWidget,
    QVBoxLayout, QAbstractItemView,
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QIcon, QDesktopServices


class PlacesSidebar(QListWidget):
    """Dolphin 风格 Places 侧边栏"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("PlacesSidebar")
        self.setMaximumWidth(200)
        self.setMinimumWidth(140)
        self.setFrameShape(QListWidget.Shape.NoFrame)
        self.setAlternatingRowColors(False)
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # 点击位置时发出信号
        self.location_selected = None  # 由外部赋值

        self._populate()
        self.itemClicked.connect(self._on_item_clicked)

    def _populate(self):
        """填充 Places"""
        places = [
            ("user-home", "主文件夹", None),
            ("folder-desktop", "桌面", "Desktop"),
            ("folder-documents", "文档", "Documents"),
            ("folder-download", "下载", "Downloads"),
            ("folder-music", "音乐", "Music"),
            ("folder-pictures", "图片", "Pictures"),
            ("folder-videos", "视频", "Videos"),
            ("folder", "根目录", "/"),
        ]

        for icon_name, name, path in places:
            item = QListWidgetItem(name)
            item.setData(Qt.ItemDataRole.UserRole, path)
            item.setIcon(self._get_icon(icon_name))
            self.addItem(item)

    def _get_icon(self, name: str) -> QIcon:
        """使用 Qt 内置图标作为后备"""
        # PySide6 有 QStyle.StandardPixmap
        from PySide6.QtWidgets import QStyle
        style = self.style()
        sp = {
            "user-home": QStyle.StandardPixmap.SP_DirHomeIcon,
            "folder-desktop": QStyle.StandardPixmap.SP_DesktopIcon,
            "folder-documents": QStyle.StandardPixmap.SP_DirIcon,
            "folder-download": QStyle.StandardPixmap.SP_DirIcon,
            "folder-music": QStyle.StandardPixmap.SP_DirIcon,
            "folder-pictures": QStyle.StandardPixmap.SP_DirIcon,
            "folder-videos": QStyle.StandardPixmap.SP_DirIcon,
            "folder": QStyle.StandardPixmap.SP_DirIcon,
        }
        standard = sp.get(name, QStyle.StandardPixmap.SP_DirIcon)
        return style.standardIcon(standard)

    def _on_item_clicked(self, item: QListWidgetItem):
        path = item.data(Qt.ItemDataRole.UserRole)
        if path and self.location_selected:
            self.location_selected(path)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
