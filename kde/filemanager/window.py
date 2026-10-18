"""
Dolphin 风格文件管理器主窗口。
"""
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QToolBar, QStatusBar, QLabel, QPushButton,
    QComboBox, QStyle, QApplication,
)
from PySide6.QtCore import Qt, QDir
from PySide6.QtGui import QIcon, QAction, QKeySequence

from ..widgets.frameless import FramelessWindow
from .sidebar import PlacesSidebar
from .breadcrumb import BreadcrumbBar
from .filelist import FileListView


class FileManagerWindow(FramelessWindow):
    """Dolphin 风格文件管理器"""

    def __init__(self):
        super().__init__("Dolphin — KDEify", 900, 600)
        self._setup_ui()
        self._setup_titlebar()

    def _setup_titlebar(self):
        self.set_window_icon(self.style().standardIcon(QStyle.StandardPixmap.SP_DirHomeIcon))

    def _setup_ui(self):
        # 创建中心控件
        central = QWidget(self)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 工具栏
        toolbar = self._create_toolbar()
        layout.addWidget(toolbar)

        # 分割器：侧边栏 + 主区域
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # 侧边栏
        self.sidebar = PlacesSidebar(self)
        self.sidebar.location_selected = self._on_location_selected
        splitter.addWidget(self.sidebar)

        # 右侧区域
        right_widget = QWidget(self)
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # 面包屑导航
        self.breadcrumb = BreadcrumbBar(self)
        self.breadcrumb.path_changed = self._on_path_changed
        right_layout.addWidget(self.breadcrumb)

        # 文件列表
        self.filelist = FileListView(self)
        self.filelist.directory_changed = self._on_path_changed
        right_layout.addWidget(self.filelist)

        splitter.addWidget(right_widget)
        splitter.setSizes([180, 720])

        layout.addWidget(splitter)

        # 状态栏
        self.statusbar = QStatusBar(self)
        self.statusbar.showMessage(f"就绪 — {self.filelist.get_path()}")
        layout.addWidget(self.statusbar)

        # 绑定信号
        self.filelist.file_activated = self._on_file_activated

        self.set_content(central)

        # 设置初始路径
        self.filelist.set_root(QDir.homePath())

    def _create_toolbar(self) -> QToolBar:
        toolbar = QToolBar(self)
        toolbar.setMovable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        # 视图切换
        self.view_combo = QComboBox(self)
        self.view_combo.addItems(["图标视图", "列表视图", "详细视图"])
        self.view_combo.currentTextChanged.connect(self._on_view_changed)
        toolbar.addWidget(QLabel("视图: "))
        toolbar.addWidget(self.view_combo)

        toolbar.addSeparator()

        # 新建文件夹
        act_new = QPushButton("新建文件夹", self)
        act_new.clicked.connect(self.filelist._new_folder)
        toolbar.addWidget(act_new)

        # 排序
        toolbar.addWidget(QLabel("排序: "))
        self.sort_combo = QComboBox(self)
        self.sort_combo.addItems(["名称", "大小", "类型", "修改时间"])
        toolbar.addWidget(self.sort_combo)

        return toolbar

    def _on_location_selected(self, path: str):
        if path is None:
            return
        # 映射逻辑目录到真实路径
        home = QDir.homePath()
        mapping = {
            "Desktop": os.path.join(home, "Desktop"),
            "Documents": os.path.join(home, "Documents"),
            "Downloads": os.path.join(home, "Downloads"),
            "Music": os.path.join(home, "Music"),
            "Pictures": os.path.join(home, "Pictures"),
            "Videos": os.path.join(home, "Videos"),
        }
        real_path = mapping.get(path, path)
        if os.path.exists(real_path):
            self.filelist.set_root(real_path)

    def _on_path_changed(self, path: str):
        self.breadcrumb.set_path(path)
        self.statusbar.showMessage(f"{path} — {self._count_items(path)} 个项目")

    def _on_file_activated(self, path: str):
        self.statusbar.showMessage(f"已打开: {path}")

    def _on_view_changed(self, text: str):
        mode_map = {
            "图标视图": "icons",
            "列表视图": "list",
            "详细视图": "details",
        }
        mode = mode_map.get(text, "details")
        self.filelist.set_view_mode(mode)

    @staticmethod
    def _count_items(path: str) -> int:
        try:
            return len(os.listdir(path))
        except (PermissionError, OSError):
            return 0
