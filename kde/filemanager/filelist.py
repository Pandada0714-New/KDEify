"""
Dolphin 风格文件列表 - 支持图标视图、列表视图、详细视图。
"""
import os
from PySide6.QtWidgets import (
    QTableView, QHeaderView, QAbstractItemView, QMenu,
    QMessageBox, QInputDialog, QLabel, QVBoxLayout,
    QWidget, QStyle, QApplication,
)
from PySide6.QtCore import Qt, QDir, QSortFilterProxyModel, QModelIndex, QTimer, QSettings
from PySide6.QtGui import QFileSystemModel, QIcon, QAction, QKeySequence, QDesktopServices, QUrl


class FileListView(QTableView):
    """文件列表视图"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("FileListView")
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setSortingEnabled(True)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setDefaultSectionSize(200)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)

        # 文件系统模型
        self._model = QFileSystemModel(self)
        self._model.setReadOnly(False)
        self._model.setNameFilterDisables(False)
        self._model.setRootPath(QDir.homePath())

        # 代理模型用于排序
        self._proxy = QSortFilterProxyModel(self)
        self._proxy.setSourceModel(self._model)
        self._proxy.setSortCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        self.setModel(self._proxy)
        self.doubleClicked.connect(self._on_double_click)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

        # 信号
        self.file_activated = None   # 双击文件/目录
        self.directory_changed = None  # 目录变化
        self.current_path = ""      # 当前路径

        # 视图模式
        self._view_mode = "details"  # icons, list, details

        # 剪切/复制缓冲区
        self._clipboard_paths = []
        self._clipboard_action = None  # "cut" or "copy"

        self.set_root(QDir.homePath())

    def set_root(self, path: str):
        """设置根目录"""
        self.current_path = path
        source_index = self._model.setRootPath(path)
        proxy_index = self._proxy.mapFromSource(source_index)
        self.setRootIndex(proxy_index)
        # 调整列宽
        self._adjust_columns()
        if self.directory_changed:
            self.directory_changed(path)

    def get_path(self) -> str:
        return self.current_path

    def _adjust_columns(self):
        if self._view_mode == "details":
            self.setColumnWidth(0, 260)
            self.setColumnWidth(1, 100)
            self.setColumnWidth(2, 100)
            self.setColumnWidth(3, 160)

    def _on_double_click(self, index: QModelIndex):
        """双击：打开文件或进入目录"""
        proxy_index = self._proxy.mapToSource(index)
        path = self._model.filePath(proxy_index)
        if os.path.isdir(path):
            self.set_root(path)
        else:
            # 用默认程序打开
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))
            if self.file_activated:
                self.file_activated(path)

    def _show_context_menu(self, pos):
        """右键菜单"""
        menu = QMenu(self)

        selected = self._selected_paths()
        if selected:
            # 打开
            act_open = menu.addAction("打开")
            act_open.triggered.connect(lambda: self._open_selected(selected))

            menu.addSeparator()

            # 剪切/复制
            act_cut = menu.addAction("剪切")
            act_cut.triggered.connect(lambda: self._set_clipboard(selected, "cut"))
            act_copy = menu.addAction("复制")
            act_copy.triggered.connect(lambda: self._set_clipboard(selected, "copy"))

            menu.addSeparator()

            # 重命名
            if len(selected) == 1:
                act_rename = menu.addAction("重命名")
                act_rename.triggered.connect(lambda: self._rename(selected[0]))

            # 删除
            act_delete = menu.addAction("删除")
            act_delete.triggered.connect(lambda: self._delete(selected))

            menu.addSeparator()

            # 属性
            if len(selected) == 1:
                act_props = menu.addAction("属性")
                act_props.triggered.connect(lambda: self._show_properties(selected[0]))
        else:
            # 空白处右键
            act_paste = menu.addAction("粘贴")
            act_paste.setEnabled(bool(self._clipboard_paths))
            act_paste.triggered.connect(self._paste)

            menu.addSeparator()

            act_new_folder = menu.addAction("新建文件夹")
            act_new_folder.triggered.connect(self._new_folder)
            act_new_file = menu.addAction("新建文件")
            act_new_file.triggered.connect(self._new_file)

            menu.addSeparator()

            act_refresh = menu.addAction("刷新")
            act_refresh.triggered.connect(lambda: self.set_root(self.current_path))

        menu.exec(self.viewport().mapToGlobal(pos))

    def _selected_paths(self) -> list:
        """获取选中的文件路径列表"""
        paths = []
        for index in self.selectedIndexes():
            if index.column() != 0:
                continue
            proxy_idx = self._proxy.mapToSource(index)
            path = self._model.filePath(proxy_idx)
            if path:
                paths.append(path)
        return paths

    def _open_selected(self, paths: list):
        for path in paths:
            if os.path.isdir(path):
                self.set_root(path)
            else:
                QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    def _set_clipboard(self, paths: list, action: str):
        self._clipboard_paths = list(paths)
        self._clipboard_action = action

    def _paste(self):
        """粘贴"""
        if not self._clipboard_paths or not self._clipboard_action:
            return
        import shutil
        dest = self.current_path
        for src in self._clipboard_paths:
            try:
                name = os.path.basename(src)
                target = os.path.join(dest, name)
                if self._clipboard_action == "cut":
                    shutil.move(src, target)
                else:
                    if os.path.isdir(src):
                        shutil.copytree(src, target, dirs_exist_ok=True)
                    else:
                        shutil.copy2(src, target)
            except Exception as e:
                QMessageBox.warning(self, "粘贴失败", f"{src}\n{e}")
                return
        if self._clipboard_action == "cut":
            self._clipboard_paths = []
            self._clipboard_action = None
        # 刷新
        self.set_root(self.current_path)

    def _rename(self, path: str):
        name = os.path.basename(path)
        new_name, ok = QInputDialog.getText(self, "重命名", "新名称：", text=name)
        if ok and new_name and new_name != name:
            new_path = os.path.join(os.path.dirname(path), new_name)
            try:
                os.rename(path, new_path)
                self.set_root(self.current_path)
            except Exception as e:
                QMessageBox.warning(self, "重命名失败", str(e))

    def _delete(self, paths: list):
        confirm = QMessageBox.question(
            self, "确认删除",
            f"确定要删除选中的 {len(paths)} 个项目吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return
        import shutil
        for path in paths:
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            except Exception as e:
                QMessageBox.warning(self, "删除失败", f"{path}\n{e}")
                return
        self.set_root(self.current_path)

    def _show_properties(self, path: str):
        """显示属性对话框"""
        info = []
        info.append(f"名称: {os.path.basename(path)}")
        info.append(f"路径: {path}")
        info.append(f"类型: {'文件夹' if os.path.isdir(path) else '文件'}")
        if os.path.isfile(path):
            size = os.path.getsize(path)
            info.append(f"大小: {self._format_size(size)}")
        info.append(f"修改时间: {os.path.getmtime(path)}")
        QMessageBox.information(self, "属性", "\n".join(info))

    @staticmethod
    def _format_size(size: int) -> str:
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} PB"

    def _new_folder(self):
        name, ok = QInputDialog.getText(self, "新建文件夹", "文件夹名称：")
        if ok and name:
            path = os.path.join(self.current_path, name)
            try:
                os.makedirs(path, exist_ok=True)
                self.set_root(self.current_path)
            except Exception as e:
                QMessageBox.warning(self, "创建失败", str(e))

    def _new_file(self):
        name, ok = QInputDialog.getText(self, "新建文件", "文件名称：")
        if ok and name:
            path = os.path.join(self.current_path, name)
            try:
                with open(path, "w") as f:
                    f.write("")
                self.set_root(self.current_path)
            except Exception as e:
                QMessageBox.warning(self, "创建失败", str(e))

    def set_view_mode(self, mode: str):
        """切换视图模式: icons / list / details"""
        self._view_mode = mode
        if mode == "details":
            self.verticalHeader().setVisible(False)
            self.horizontalHeader().setVisible(True)
            self.setColumnWidth(0, 260)
        elif mode == "list":
            self.verticalHeader().setVisible(True)
            self.setColumnWidth(0, 400)
            self.setRowHeight(0, 24)
        else:
            self.verticalHeader().setVisible(True)
            self.setRowHeight(0, 80)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            paths = self._selected_paths()
            if paths:
                self._delete(paths)
        elif event.key() == Qt.Key.Key_F2:
            paths = self._selected_paths()
            if len(paths) == 1:
                self._rename(paths[0])
        elif event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            paths = self._selected_paths()
            if paths:
                self._open_selected(paths)
        else:
            super().keyPressEvent(event)
