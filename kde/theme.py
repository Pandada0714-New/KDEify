"""
Breeze 主题 - KDE Plasma 默认主题的颜色和 QSS 样式表。

颜色参考：
    https://develop.kde.org/hig/style/color/default/
"""
from PySide6.QtGui import QColor


# ──────────────────────────────────────────────
# Breeze 调色板
# ──────────────────────────────────────────────
class BreezeColors:
    """Breeze 主题核心颜色"""

    # 基础背景
    WindowBackground_Light = QColor("#eff0f1")
    WindowBackground_Dark  = QColor("#232629")

    # 控件背景
    ViewBackground_Light   = QColor("#fcfcfc")
    ViewBackground_Dark    = QColor("#2a2e32")

    # 前景/文字
    Foreground_Light       = QColor("#232629")
    Foreground_Dark        = QColor("#eff0f1")

    # 禁用文字
    DisabledForeground_Light = QColor("#bdc3c7")
    DisabledForeground_Dark  = QColor("#6d6d6d")

    # 高亮/选中
    Highlight_Light        = QColor("#3daee9")
    Highlight_Dark         = QColor("#3daee9")
    HighlightForeground_Light = QColor("#ffffff")
    HighlightForeground_Dark  = QColor("#ffffff")

    # 边框
    Border_Light           = QColor("#bdc3c7")
    Border_Dark            = QColor("#3f4447")

    # 按钮
    ButtonBackground_Light = QColor("#fcfcfc")
    ButtonBackground_Dark  = QColor("#31363b")
    ButtonForeground_Light = QColor("#232629")
    ButtonForeground_Dark  = QColor("#eff0f1")

    # 悬停
    Hover_Light            = QColor("#e3f0f6")
    Hover_Dark             = QColor("#3daee9")
    HoverForeground_Light      = QColor("#3daee9")
    HoverForeground_Dark       = QColor("#ffffff")

    # 选中行
    Selection_Light        = QColor("#3daee9")
    Selection_Dark         = QColor("#3daee9")

    # 链接
    Link_Light             = QColor("#2980b9")
    Link_Dark              = QColor("#1d99f3")

    # 工具提示
    TipBackground_Light    = QColor("#fcfcfc")
    TipBackground_Dark     = QColor("#31363b")
    TipForeground_Light    = QColor("#232629")
    TipForeground_Dark     = QColor("#eff0f1")

    # 错误/警告
    ErrorBackground        = QColor("#da4453")
    WarningBackground      = QColor("#f67400")
    SuccessBackground      = QColor("#27ae60")

    # 交替行
    Alternate_Light        = QColor("#f5f5f5")
    Alternate_Dark         = QColor("#2c3034")


# ──────────────────────────────────────────────
# Breeze 全局 QSS
# ──────────────────────────────────────────────
LIGHT_QSS = """
/* ── 全局 ── */
QWidget {
    font-family: "Noto Sans", "Segoe UI", "Microsoft YaHei", sans-serif;
    font-size: 9pt;
    color: #232629;
    background-color: #eff0f1;
    selection-background-color: #3daee9;
    selection-color: #ffffff;
}

QMainWindow, QDialog {
    background-color: #eff0f1;
    border: 1px solid #bdc3c7;
}

/* ── 分组框 ── */
QGroupBox {
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    margin-top: 10px;
    padding-top: 6px;
    background-color: #fcfcfc;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 4px;
    color: #232629;
}

/* ── 按钮 ── */
QPushButton {
    background-color: #fcfcfc;
    color: #232629;
    border: 1px solid #bdc3c7;
    border-radius: 3px;
    padding: 4px 12px;
    min-width: 70px;
    min-height: 24px;
}
QPushButton:hover {
    background-color: #e3f0f6;
    color: #3daee9;
    border-color: #3daee9;
}
QPushButton:pressed {
    background-color: #3daee9;
    color: #ffffff;
    border-color: #3daee9;
}
QPushButton:disabled {
    color: #bdc3c7;
    background-color: #eff0f1;
    border-color: #d6d9dc;
}
QPushButton:checked {
    background-color: #3daee9;
    color: #ffffff;
    border-color: #3daee9;
}

/* ── 输入框 ── */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #fcfcfc;
    border: 1px solid #bdc3c7;
    border-radius: 3px;
    padding: 2px 4px;
    selection-background-color: #3daee9;
    selection-color: #ffffff;
}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #3daee9;
}
QLineEdit:disabled, QTextEdit:disabled {
    background-color: #eff0f1;
    color: #bdc3c7;
}

/* ── 下拉框 ── */
QComboBox {
    background-color: #fcfcfc;
    border: 1px solid #bdc3c7;
    border-radius: 3px;
    padding: 2px 4px;
    min-height: 24px;
}
QComboBox:hover {
    border-color: #3daee9;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #232629;
    margin-right: 6px;
}
QComboBox QAbstractItemView {
    background-color: #fcfcfc;
    border: 1px solid #bdc3c7;
    selection-background-color: #3daee9;
    selection-color: #ffffff;
}

/* ── 列表/树/表 ── */
QListWidget, QTreeView, QTableView, QListView {
    background-color: #fcfcfc;
    border: 1px solid #bdc3c7;
    alternate-background-color: #f5f5f5;
    outline: 0;
}
QListWidget::item, QTreeView::item, QTableView::item, QListView::item {
    padding: 4px 6px;
    border: none;
}
QListWidget::item:hover, QTreeView::item:hover,
QTableView::item:hover, QListView::item:hover {
    background-color: #e3f0f6;
    color: #3daee9;
}
QListWidget::item:selected, QTreeView::item:selected,
QTableView::item:selected, QListView::item:selected {
    background-color: #3daee9;
    color: #ffffff;
}
QHeaderView::section {
    background-color: #eff0f1;
    color: #232629;
    border: none;
    border-bottom: 1px solid #bdc3c7;
    border-right: 1px solid #d6d9dc;
    padding: 4px 6px;
    min-height: 28px;
}
QHeaderView::section:hover {
    background-color: #e3f0f6;
}

/* ── 菜单 ── */
QMenuBar {
    background-color: #eff0f1;
    border-bottom: 1px solid #bdc3c7;
    padding: 2px;
}
QMenuBar::item {
    background: transparent;
    padding: 4px 10px;
    border-radius: 3px;
}
QMenuBar::item:selected {
    background-color: #e3f0f6;
    color: #3daee9;
}
QMenuBar::item:pressed {
    background-color: #3daee9;
    color: #ffffff;
}
QMenu {
    background-color: #fcfcfc;
    border: 1px solid #bdc3c7;
    padding: 4px;
}
QMenu::item {
    padding: 6px 24px 6px 24px;
    border-radius: 3px;
}
QMenu::item:selected {
    background-color: #3daee9;
    color: #ffffff;
}
QMenu::separator {
    height: 1px;
    background-color: #bdc3c7;
    margin: 4px 8px;
}

/* ── 工具栏 ── */
QToolBar {
    background-color: #eff0f1;
    border-bottom: 1px solid #bdc3c7;
    spacing: 2px;
    padding: 2px;
}
QToolBar::separator {
    width: 1px;
    background-color: #bdc3c7;
    margin: 2px 4px;
}

/* ── 标签页 ── */
QTabWidget::pane {
    border: 1px solid #bdc3c7;
    border-radius: 3px;
    background-color: #fcfcfc;
}
QTabBar::tab {
    background-color: #eff0f1;
    color: #232629;
    border: 1px solid #bdc3c7;
    border-bottom: none;
    border-top-left-radius: 3px;
    border-top-right-radius: 3px;
    padding: 6px 14px;
    margin-right: 1px;
}
QTabBar::tab:hover {
    background-color: #e3f0f6;
    color: #3daee9;
}
QTabBar::tab:selected {
    background-color: #fcfcfc;
    color: #232629;
    border-top: 2px solid #3daee9;
    padding-top: 4px;
}

/* ── 滚动条 ── */
QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background: #bdc3c7;
    border-radius: 4px;
    min-height: 30px;
    margin: 2px;
}
QScrollBar::handle:vertical:hover {
    background: #3daee9;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
QScrollBar:horizontal {
    background: transparent;
    height: 10px;
    margin: 0;
}
QScrollBar::handle:horizontal {
    background: #bdc3c7;
    border-radius: 4px;
    min-width: 30px;
    margin: 2px;
}
QScrollBar::handle:horizontal:hover {
    background: #3daee9;
}

/* ── 状态栏 ── */
QStatusBar {
    background-color: #eff0f1;
    border-top: 1px solid #bdc3c7;
    padding: 2px 6px;
}
QStatusBar::item {
    border: none;
}

/* ── 工具提示 ── */
QToolTip {
    background-color: #fcfcfc;
    color: #232629;
    border: 1px solid #bdc3c7;
    padding: 4px 8px;
}

/* ── 进度条 ── */
QProgressBar {
    background-color: #d6d9dc;
    border: 1px solid #bdc3c7;
    border-radius: 3px;
    text-align: center;
    color: #232629;
}
QProgressBar::chunk {
    background-color: #3daee9;
    border-radius: 2px;
}

/* ── 滑块 ── */
QSlider::groove:horizontal {
    height: 4px;
    background: #bdc3c7;
    border-radius: 2px;
}
QSlider::handle:horizontal {
    background: #fcfcfc;
    border: 1px solid #bdc3c7;
    width: 14px;
    height: 14px;
    margin: -6px 0;
    border-radius: 7px;
}
QSlider::handle:horizontal:hover {
    background: #3daee9;
    border-color: #3daee9;
}
QSlider::sub-page:horizontal {
    background: #3daee9;
    border-radius: 2px;
}

/* ── 单选/复选 ── */
QRadioButton::indicator, QCheckBox::indicator {
    width: 16px;
    height: 16px;
}
QRadioButton::indicator {
    border-radius: 8px;
    border: 1px solid #bdc3c7;
    background: #fcfcfc;
}
QRadioButton::indicator:checked {
    border: 1px solid #3daee9;
    background: #3daee9;
    border-radius: 8px;
}
QCheckBox::indicator {
    border: 1px solid #bdc3c7;
    border-radius: 3px;
    background: #fcfcfc;
}
QCheckBox::indicator:checked {
    background: #3daee9;
    border-color: #3daee9;
}

/* ── 分割线 ── */
QSplitter::handle {
    background-color: #bdc3c7;
}
QSplitter::handle:hover {
    background-color: #3daee9;
}
"""

DARK_QSS = """
/* ── 全局 ── */
QWidget {
    font-family: "Noto Sans", "Segoe UI", "Microsoft YaHei", sans-serif;
    font-size: 9pt;
    color: #eff0f1;
    background-color: #232629;
    selection-background-color: #3daee9;
    selection-color: #ffffff;
}

QMainWindow, QDialog {
    background-color: #232629;
    border: 1px solid #3f4447;
}

QGroupBox {
    border: 1px solid #3f4447;
    border-radius: 4px;
    margin-top: 10px;
    padding-top: 6px;
    background-color: #2a2e32;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 4px;
    color: #eff0f1;
}

QPushButton {
    background-color: #31363b;
    color: #eff0f1;
    border: 1px solid #3f4447;
    border-radius: 3px;
    padding: 4px 12px;
    min-width: 70px;
    min-height: 24px;
}
QPushButton:hover {
    background-color: #3daee9;
    color: #ffffff;
    border-color: #3daee9;
}
QPushButton:pressed {
    background-color: #3daee9;
    color: #ffffff;
    border-color: #3daee9;
}
QPushButton:disabled {
    color: #6d6d6d;
    background-color: #232629;
    border-color: #3f4447;
}
QPushButton:checked {
    background-color: #3daee9;
    color: #ffffff;
    border-color: #3daee9;
}

QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #2a2e32;
    border: 1px solid #3f4447;
    border-radius: 3px;
    padding: 2px 4px;
    selection-background-color: #3daee9;
    selection-color: #ffffff;
}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #3daee9;
}
QLineEdit:disabled, QTextEdit:disabled {
    background-color: #232629;
    color: #6d6d6d;
}

QComboBox {
    background-color: #31363b;
    border: 1px solid #3f4447;
    border-radius: 3px;
    padding: 2px 4px;
    min-height: 24px;
}
QComboBox:hover {
    border-color: #3daee9;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #eff0f1;
    margin-right: 6px;
}
QComboBox QAbstractItemView {
    background-color: #2a2e32;
    border: 1px solid #3f4447;
    selection-background-color: #3daee9;
    selection-color: #ffffff;
}

QListWidget, QTreeView, QTableView, QListView {
    background-color: #2a2e32;
    border: 1px solid #3f4447;
    alternate-background-color: #2c3034;
    outline: 0;
}
QListWidget::item, QTreeView::item, QTableView::item, QListView::item {
    padding: 4px 6px;
    border: none;
}
QListWidget::item:hover, QTreeView::item:hover,
QTableView::item:hover, QListView::item:hover {
    background-color: #3daee9;
    color: #ffffff;
}
QListWidget::item:selected, QTreeView::item:selected,
QTableView::item:selected, QListView::item:selected {
    background-color: #3daee9;
    color: #ffffff;
}
QHeaderView::section {
    background-color: #232629;
    color: #eff0f1;
    border: none;
    border-bottom: 1px solid #3f4447;
    border-right: 1px solid #33373a;
    padding: 4px 6px;
    min-height: 28px;
}
QHeaderView::section:hover {
    background-color: #3daee9;
}

QMenuBar {
    background-color: #232629;
    border-bottom: 1px solid #3f4447;
    padding: 2px;
}
QMenuBar::item {
    background: transparent;
    padding: 4px 10px;
    border-radius: 3px;
}
QMenuBar::item:selected {
    background-color: #3daee9;
    color: #ffffff;
}
QMenuBar::item:pressed {
    background-color: #3daee9;
    color: #ffffff;
}
QMenu {
    background-color: #2a2e32;
    border: 1px solid #3f4447;
    padding: 4px;
}
QMenu::item {
    padding: 6px 24px 6px 24px;
    border-radius: 3px;
}
QMenu::item:selected {
    background-color: #3daee9;
    color: #ffffff;
}
QMenu::separator {
    height: 1px;
    background-color: #3f4447;
    margin: 4px 8px;
}

QToolBar {
    background-color: #232629;
    border-bottom: 1px solid #3f4447;
    spacing: 2px;
    padding: 2px;
}
QToolBar::separator {
    width: 1px;
    background-color: #3f4447;
    margin: 2px 4px;
}

QTabWidget::pane {
    border: 1px solid #3f4447;
    border-radius: 3px;
    background-color: #2a2e32;
}
QTabBar::tab {
    background-color: #232629;
    color: #eff0f1;
    border: 1px solid #3f4447;
    border-bottom: none;
    border-top-left-radius: 3px;
    border-top-right-radius: 3px;
    padding: 6px 14px;
    margin-right: 1px;
}
QTabBar::tab:hover {
    background-color: #3daee9;
    color: #ffffff;
}
QTabBar::tab:selected {
    background-color: #2a2e32;
    color: #eff0f1;
    border-top: 2px solid #3daee9;
    padding-top: 4px;
}

QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background: #3f4447;
    border-radius: 4px;
    min-height: 30px;
    margin: 2px;
}
QScrollBar::handle:vertical:hover {
    background: #3daee9;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
QScrollBar:horizontal {
    background: transparent;
    height: 10px;
    margin: 0;
}
QScrollBar::handle:horizontal {
    background: #3f4447;
    border-radius: 4px;
    min-width: 30px;
    margin: 2px;
}
QScrollBar::handle:horizontal:hover {
    background: #3daee9;
}

QStatusBar {
    background-color: #232629;
    border-top: 1px solid #3f4447;
    padding: 2px 6px;
}
QStatusBar::item {
    border: none;
}

QToolTip {
    background-color: #31363b;
    color: #eff0f1;
    border: 1px solid #3f4447;
    padding: 4px 8px;
}

QProgressBar {
    background-color: #3f4447;
    border: 1px solid #3f4447;
    border-radius: 3px;
    text-align: center;
    color: #eff0f1;
}
QProgressBar::chunk {
    background-color: #3daee9;
    border-radius: 2px;
}

QSlider::groove:horizontal {
    height: 4px;
    background: #3f4447;
    border-radius: 2px;
}
QSlider::handle:horizontal {
    background: #31363b;
    border: 1px solid #3f4447;
    width: 14px;
    height: 14px;
    margin: -6px 0;
    border-radius: 7px;
}
QSlider::handle:horizontal:hover {
    background: #3daee9;
    border-color: #3daee9;
}
QSlider::sub-page:horizontal {
    background: #3daee9;
    border-radius: 2px;
}

QRadioButton::indicator, QCheckBox::indicator {
    width: 16px;
    height: 16px;
}
QRadioButton::indicator {
    border-radius: 8px;
    border: 1px solid #3f4447;
    background: #2a2e32;
}
QRadioButton::indicator:checked {
    border: 1px solid #3daee9;
    background: #3daee9;
    border-radius: 8px;
}
QCheckBox::indicator {
    border: 1px solid #3f4447;
    border-radius: 3px;
    background: #2a2e32;
}
QCheckBox::indicator:checked {
    background: #3daee9;
    border-color: #3daee9;
}

QSplitter::handle {
    background-color: #3f4447;
}
QSplitter::handle:hover {
    background-color: #3daee9;
}
"""

# ──────────────────────────────────────────────
# 标题栏专用 QSS
# ──────────────────────────────────────────────
TITLEBAR_QSS = """
#TitleBar {
    background-color: #232629;
    min-height: 30px;
    max-height: 30px;
}
#TitleBar QLabel#TitleLabel {
    color: #eff0f1;
    font-size: 9pt;
    padding-left: 8px;
}
#TitleBar QPushButton {
    background: transparent;
    border: none;
    border-radius: 0;
    min-width: 40px;
    max-width: 40px;
    min-height: 30px;
    max-height: 30px;
    padding: 0;
}
#TitleBar QPushButton:hover {
    background-color: #3f4447;
}
#TitleBar QPushButton#CloseButton:hover {
    background-color: #da4453;
    color: #ffffff;
}
#TitleBar QPushButton:pressed {
    background-color: #3daee9;
    color: #ffffff;
}
"""

DARK_TITLEBAR_QSS = TITLEBAR_QSS
