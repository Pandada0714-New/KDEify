"""KDEify 应用核心 - QApplication 和主题管理"""
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSettings

from .theme import LIGHT_QSS, DARK_QSS


# QSettings 存储位置（Windows 注册表）
APP_ORG = "KDEify"
APP_NAME = "KDEify"


class KDEApplication(QApplication):
    """全局 QApplication，负责加载主题"""

    def __init__(self, argv):
        super().__init__(argv)
        self.setApplicationName("KDEify")
        self.setOrganizationName("KDEify")
        self._settings = QSettings(APP_ORG, APP_NAME)
        self._dark_mode = self._settings.value("dark_mode", "false").lower() == "true"

    @property
    def settings(self) -> QSettings:
        return self._settings

    @property
    def is_dark(self) -> bool:
        return self._dark_mode

    def apply_theme(self, dark: bool = None):
        """应用全局主题"""
        if dark is not None:
            self._dark_mode = dark
        self._settings.setValue("dark_mode", str(self._dark_mode).lower())
        self._settings.sync()

        qss = DARK_QSS if self._dark_mode else LIGHT_QSS
        self.setStyleSheet(qss)

    def toggle_theme(self):
        self.apply_theme(not self._dark_mode)
        return self._dark_mode
