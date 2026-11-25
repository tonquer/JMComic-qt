"""Generate unified modern QSS stylesheets for JMComic-qt themes."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THEME_DIR = ROOT / "res" / "theme"

THEMES = {
    "dark_orange": {
        "icon_dir": "dark_orange",
        "bg_base": "#181A1F",
        "bg_sidebar": "#1E2128",
        "bg_sidebar_hover": "#282C36",
        "bg_surface": "#22252D",
        "bg_elevated": "#272B35",
        "bg_hover": "#2F3440",
        "bg_pressed": "#1D2026",
        "bg_alt": "#1D2026",
        "border": "#2E333E",
        "border_strong": "#3D4452",
        "divider": "#2A2F3A",
        "text": "#E8ECF2",
        "text_muted": "#94A3B8",
        "text_disabled": "rgba(232, 236, 242, 0.35)",
        "primary": "#FF8A1F",
        "primary_hover": "#FF9E44",
        "primary_pressed": "#E06D06",
        "primary_soft": "rgba(255, 138, 31, 0.16)",
        "primary_soft_hover": "rgba(255, 138, 31, 0.24)",
        "primary_border_soft": "rgba(255, 138, 31, 0.45)",
        "primary_text": "#FFFFFF",
        "selection_bg": "rgba(255, 138, 31, 0.35)",
        "selection_text": "#FFFFFF",
        "scroll_handle": "rgba(148, 163, 184, 0.32)",
        "scroll_handle_hover": "rgba(255, 138, 31, 0.78)",
        "main_border": "#2E333E",
        "slider_groove": "#2E333E",
        "progress_bg": "#2A2F3A",
        "danger": "#EF4444",
        "danger_soft": "rgba(239, 68, 68, 0.16)",
        "warning": "#F59E0B",
        "warning_soft": "rgba(245, 158, 11, 0.16)",
        "success": "#10B981",
        "success_soft": "rgba(16, 185, 129, 0.16)",
    },
    "dark_pink": {
        "icon_dir": "dark_pink",
        "bg_base": "#181A1F",
        "bg_sidebar": "#1E2128",
        "bg_sidebar_hover": "#282C36",
        "bg_surface": "#22252D",
        "bg_elevated": "#272B35",
        "bg_hover": "#2F3440",
        "bg_pressed": "#1D2026",
        "bg_alt": "#1D2026",
        "border": "#2E333E",
        "border_strong": "#3D4452",
        "divider": "#2A2F3A",
        "text": "#E8ECF2",
        "text_muted": "#94A3B8",
        "text_disabled": "rgba(232, 236, 242, 0.35)",
        "primary": "#F45B93",
        "primary_hover": "#F777A6",
        "primary_pressed": "#D8437A",
        "primary_soft": "rgba(244, 91, 147, 0.16)",
        "primary_soft_hover": "rgba(244, 91, 147, 0.24)",
        "primary_border_soft": "rgba(244, 91, 147, 0.45)",
        "primary_text": "#FFFFFF",
        "selection_bg": "rgba(244, 91, 147, 0.35)",
        "selection_text": "#FFFFFF",
        "scroll_handle": "rgba(148, 163, 184, 0.32)",
        "scroll_handle_hover": "rgba(244, 91, 147, 0.78)",
        "main_border": "#2E333E",
        "slider_groove": "#2E333E",
        "progress_bg": "#2A2F3A",
        "danger": "#EF4444",
        "danger_soft": "rgba(239, 68, 68, 0.16)",
        "warning": "#F59E0B",
        "warning_soft": "rgba(245, 158, 11, 0.16)",
        "success": "#10B981",
        "success_soft": "rgba(16, 185, 129, 0.16)",
    },
    "light_orange": {
        "icon_dir": "light_orange",
        "bg_base": "#F8F9FB",
        "bg_sidebar": "#F1F3F6",
        "bg_sidebar_hover": "#E6E9EF",
        "bg_surface": "#FFFFFF",
        "bg_elevated": "#FFFFFF",
        "bg_hover": "#EEF1F5",
        "bg_pressed": "#E2E8F0",
        "bg_alt": "#F8FAFC",
        "border": "#E2E8F0",
        "border_strong": "#CBD5E1",
        "divider": "#E5E7EB",
        "text": "#1E293B",
        "text_muted": "#64748B",
        "text_disabled": "rgba(30, 41, 59, 0.38)",
        "primary": "#F97316",
        "primary_hover": "#FB923C",
        "primary_pressed": "#EA580C",
        "primary_soft": "rgba(249, 115, 22, 0.12)",
        "primary_soft_hover": "rgba(249, 115, 22, 0.20)",
        "primary_border_soft": "rgba(249, 115, 22, 0.40)",
        "primary_text": "#FFFFFF",
        "selection_bg": "rgba(249, 115, 22, 0.24)",
        "selection_text": "#1E293B",
        "scroll_handle": "rgba(100, 116, 139, 0.30)",
        "scroll_handle_hover": "rgba(249, 115, 22, 0.78)",
        "main_border": "#CBD5E1",
        "slider_groove": "#CBD5E1",
        "progress_bg": "#E2E8F0",
        "danger": "#DC2626",
        "danger_soft": "rgba(220, 38, 38, 0.12)",
        "warning": "#D97706",
        "warning_soft": "rgba(217, 119, 6, 0.12)",
        "success": "#059669",
        "success_soft": "rgba(5, 150, 105, 0.12)",
    },
    "light_pink": {
        "icon_dir": "light_pink",
        "bg_base": "#F8F9FB",
        "bg_sidebar": "#F1F3F6",
        "bg_sidebar_hover": "#E6E9EF",
        "bg_surface": "#FFFFFF",
        "bg_elevated": "#FFFFFF",
        "bg_hover": "#EEF1F5",
        "bg_pressed": "#E2E8F0",
        "bg_alt": "#F8FAFC",
        "border": "#E2E8F0",
        "border_strong": "#CBD5E1",
        "divider": "#E5E7EB",
        "text": "#1E293B",
        "text_muted": "#64748B",
        "text_disabled": "rgba(30, 41, 59, 0.38)",
        "primary": "#EC4899",
        "primary_hover": "#F472B6",
        "primary_pressed": "#DB2777",
        "primary_soft": "rgba(236, 72, 153, 0.12)",
        "primary_soft_hover": "rgba(236, 72, 153, 0.20)",
        "primary_border_soft": "rgba(236, 72, 153, 0.40)",
        "primary_text": "#FFFFFF",
        "selection_bg": "rgba(236, 72, 153, 0.24)",
        "selection_text": "#1E293B",
        "scroll_handle": "rgba(100, 116, 139, 0.30)",
        "scroll_handle_hover": "rgba(236, 72, 153, 0.78)",
        "main_border": "#CBD5E1",
        "slider_groove": "#CBD5E1",
        "progress_bg": "#E2E8F0",
        "danger": "#DC2626",
        "danger_soft": "rgba(220, 38, 38, 0.12)",
        "warning": "#D97706",
        "warning_soft": "rgba(217, 119, 6, 0.12)",
        "success": "#059669",
        "success_soft": "rgba(5, 150, 105, 0.12)",
    },
}

QSS_TEMPLATE = """/* ------------------------------------------------------------------------ */
/* JMComic-qt Modern Theme ({name})                                         */
/* Generated by script/build_theme.py                                       */
/* ------------------------------------------------------------------------ */

* {{
  color: {text};
  font-family: "Microsoft YaHei UI", "PingFang SC", "Segoe UI", sans-serif;
  /*replace*/
  selection-background-color: {selection_bg};
  selection-color: {selection_text};
}}

*:focus {{
  outline: none;
}}

/* ------------------------------------------------------------------------ */
/* Semantic helper classes & roles                                          */

.danger,
QLabel[role="danger"] {{
  color: {danger};
}}

.warning,
QLabel[role="warning"] {{
  color: {warning};
}}

.success,
QLabel[role="success"] {{
  color: {success};
}}

QLabel[role="muted"] {{
  color: {text_muted};
}}

QLabel[role="sectionTitle"] {{
  color: {primary};
  font-weight: 600;
}}

QLabel[role="pageTitle"] {{
  color: {text};
  font-size: 18px;
  font-weight: 700;
}}

QLabel[role="cardTitle"] {{
  color: {text};
  font-weight: 600;
}}

QLabel[role="breadcrumbSep"] {{
  color: {text_muted};
  padding: 0 2px;
}}

QFrame[role="card"],
QWidget[role="card"] {{
  background-color: {bg_surface};
  border: 1px solid {border};
  border-radius: 10px;
}}

/* Modal dialog card */
QWidget#centerWidget {{
  background-color: {bg_surface};
  border: 1px solid {border_strong};
  border-radius: 12px;
}}

/* Top breadcrumb header bar */
QWidget#headerBar {{
  background-color: {bg_base};
  border-bottom: 1px solid {divider};
}}

QWidget#headerBar QToolButton {{
  height: 28px;
  padding: 2px 10px;
  border-radius: 6px;
  color: {text_muted};
  font-weight: 500;
}}

QWidget#headerBar QToolButton:hover {{
  color: {text};
  background-color: {bg_hover};
}}

QWidget#headerBar QToolButton:checked {{
  color: {text};
  background-color: transparent;
  font-weight: 600;
}}

/* Setting & Login cards */
SettingView QScrollArea .QFrame,
LoginNewView QWidget#tab_4 .QFrame {{
  background-color: {bg_surface};
  border: 1px solid {border};
  border-radius: 10px;
}}

LoginNewView QWidget#widget {{
  background-color: {bg_surface};
  border: 1px solid {border};
  border-radius: 12px;
}}

/* ------------------------------------------------------------------------ */
/* Base containers                                                          */

QWidget {{
  /*replace*/
  background-color: {bg_base};
}}

QWidget#MainWindows {{
  border: 1px solid {main_border};
  border-radius: 10px;
}}

QFrame {{
  background-color: {bg_base};
  border: 1px solid {border};
  border-radius: 6px;
}}

QSplitter {{
  background-color: transparent;
  border: none;
}}

QSplitter::handle {{
  background-color: transparent;
}}

QStatusBar {{
  color: {text_muted};
  background-color: {bg_surface};
  border-top: 1px solid {divider};
  border-radius: 0px;
}}

QScrollArea,
QStackedWidget,
QWidget > QToolBox,
QToolBox > QWidget,
QTabWidget > QWidget {{
  border: none;
}}

QTabWidget::pane {{
  border: none;
  background-color: transparent;
}}

QListWidget,
QScrollArea {{
  background-color: transparent;
  border: none;
}}

QToolTip {{
  color: {text};
  background-color: {bg_elevated};
  border: 1px solid {border_strong};
  border-radius: 6px;
  padding: 6px 10px;
}}

/* ------------------------------------------------------------------------ */
/* Sidebar Navigation                                                       */

NavigationWidget,
NavigationWidget > QWidget,
NavigationWidget QWidget#topWidget,
NavigationWidget QScrollArea,
NavigationWidget QScrollArea > QWidget,
NavigationWidget QWidget#scrollAreaWidgetContents {{
  background-color: {bg_sidebar};
}}

NavigationWidget {{
  border-right: 1px solid {divider};
}}

NavigationWidget QLabel#label,
NavigationWidget QLabel#label_2,
NavigationWidget QLabel#label_3 {{
  color: {text_muted};
  font-weight: 600;
  padding: 8px 12px 2px 12px;
}}

NavigationWidget QLabel#label_4,
NavigationWidget QLabel#label_5,
NavigationWidget QLabel#label_6,
NavigationWidget QLabel#label_7,
NavigationWidget QLabel#label_8,
NavigationWidget QLabel#label_9,
NavigationWidget QLabel#expLabel {{
  color: {text_muted};
}}

NavigationWidget QLabel#nameLabel {{
  color: {text};
  font-size: 13px;
  font-weight: 600;
}}

NavigationWidget QLabel#titleLabel {{
  color: {primary};
  font-size: 11px;
}}

NavigationWidget QToolButton {{
  height: 36px;
  margin: 2px 8px;
  padding: 4px 12px;
  border-radius: 8px;
  text-align: left;
}}

NavigationWidget QToolButton:hover {{
  background-color: {bg_sidebar_hover};
}}

NavigationWidget QToolButton:checked {{
  background-color: {primary_soft};
  color: {primary};
  font-weight: 600;
  border-left: 3px solid {primary};
  border-top-left-radius: 2px;
  border-bottom-left-radius: 2px;
  border-top-right-radius: 8px;
  border-bottom-right-radius: 8px;
  padding-left: 9px;
}}

NavigationWidget QToolButton:checked:hover {{
  background-color: {primary_soft_hover};
}}

NavigationWidget[collapsed="true"] QToolButton {{
  height: 40px;
  margin: 2px 6px;
  padding: 0px;
  border-radius: 8px;
}}

NavigationWidget[collapsed="true"] QToolButton:checked {{
  border-left: 3px solid {primary};
  border-top-left-radius: 2px;
  border-bottom-left-radius: 2px;
  border-top-right-radius: 8px;
  border-bottom-right-radius: 8px;
  padding-left: 0px;
}}

NavigationWidget[collapsed="true"] QFrame[frameShape="4"] {{
  margin: 4px 12px;
}}

NavigationWidget[collapsed="true"] QScrollBar:vertical {{
  width: 4px;
}}

NavigationWidget QPushButton#hideButton {{
  height: 26px;
  min-height: 26px;
  max-height: 28px;
  padding: 0px 10px;
  font-size: 12px;
  font-weight: 500;
}}

/* ------------------------------------------------------------------------ */
/* Comic Card & Comment Item                                                */

QWidget#ComicItem {{
  background-color: transparent;
  border: 1px solid transparent;
  border-radius: 10px;
}}

QWidget#ComicItem:hover {{
  background-color: {bg_surface};
  border: 1px solid {border_strong};
}}

QWidget#ComicItem QLabel#categoryLabel,
QWidget#ComicItem QLabel#timeLabel,
QWidget#ComicItem QToolButton#starButton {{
  color: {text_muted};
  font-size: 12px;
}}

QWidget#ComicItem QLabel#nameLable {{
  color: {text};
}}

QWidget#CommentItem QLabel#indexLabel,
QWidget#CommentItem QLabel#dateLabel {{
  color: {text_muted};
}}

QWidget#CommentItem QLabel#nameLabel {{
  color: {text};
  font-weight: 600;
}}

QWidget#CommentItem QLabel#levelLabel,
QWidget#CommentItem QLabel#titleLabel {{
  color: {primary};
  font-weight: 600;
}}

/* Book Detail Page */
BookInfoView QLabel#title {{
  color: {text};
  font-size: 18px;
  font-weight: 700;
}}

BookInfoView QLabel#picture {{
  background-color: transparent;
  border: none;
  padding: 6px;
}}

BookInfoView QLabel#picture[empty="true"] {{
  background-color: {bg_surface};
  border: 1px solid {border};
  border-radius: 10px;
  color: {text_muted};
}}

BookInfoView QPlainTextEdit#description {{
  background-color: {bg_surface};
  border: 1px solid {border};
  border-radius: 8px;
  padding: 8px 10px;
  color: {text};
}}

BookInfoView QLabel#label_6,
BookInfoView QLabel#label_4,
BookInfoView QLabel#label_8,
BookInfoView QLabel#label_13,
BookInfoView QLabel#label_2,
BookInfoView QLabel#label_3,
BookInfoView QLabel#label_5 {{
  color: {text_muted};
}}

/* ------------------------------------------------------------------------ */
/* Inputs                                                                   */

QDateTimeEdit,
QSpinBox,
QDoubleSpinBox,
QTextEdit,
QPlainTextEdit,
QLineEdit,
QComboBox {{
  color: {text};
  background-color: {bg_elevated};
  border: 1px solid {border};
  border-radius: 6px;
  padding: 6px 12px;
  min-height: 20px;
}}

QDateTimeEdit:hover,
QSpinBox:hover,
QDoubleSpinBox:hover,
QTextEdit:hover,
QPlainTextEdit:hover,
QLineEdit:hover,
QComboBox:hover {{
  border-color: {border_strong};
}}

QDateTimeEdit:focus,
QSpinBox:focus,
QDoubleSpinBox:focus,
QTextEdit:focus,
QPlainTextEdit:focus,
QLineEdit:focus,
QComboBox:focus,
QComboBox:on {{
  border: 1px solid {primary};
  background-color: {bg_elevated};
}}

QDateTimeEdit:disabled,
QSpinBox:disabled,
QDoubleSpinBox:disabled,
QTextEdit:disabled,
QPlainTextEdit:disabled,
QLineEdit:disabled,
QComboBox:disabled {{
  color: {text_disabled};
  background-color: {bg_alt};
  border-color: {border};
}}

QTextEdit,
QPlainTextEdit {{
  padding: 8px 10px;
}}

/* ------------------------------------------------------------------------ */
/* QComboBox                                                                */

QComboBox {{
  padding-right: 28px;
  min-height: 22px;
}}

QComboBox::drop-down {{
  subcontrol-origin: padding;
  subcontrol-position: top right;
  width: 24px;
  border: none;
  background-color: transparent;
}}

QComboBox::down-arrow {{
  image: url(:/icon/theme/{icon_dir}/primary/downarrow.svg);
  width: 12px;
  height: 12px;
  margin-right: 6px;
}}

QComboBox::down-arrow:disabled {{
  image: url(:/icon/theme/{icon_dir}/disabled/downarrow.svg);
}}

QComboBox QAbstractItemView {{
  background-color: {bg_elevated};
  color: {text};
  border: 1px solid {border_strong};
  border-radius: 8px;
  padding: 4px;
  outline: none;
  selection-background-color: {primary_soft};
  selection-color: {primary};
}}

QComboBox[frame='false'] {{
  color: {text};
  background-color: transparent;
  border: 1px solid transparent;
}}

QComboBox[frame='false']:disabled {{
  color: {text_disabled};
}}

/* ------------------------------------------------------------------------ */
/* SpinBox arrows                                                           */

QDateTimeEdit::up-button,
QDoubleSpinBox::up-button,
QSpinBox::up-button {{
  subcontrol-origin: border;
  subcontrol-position: top right;
  width: 20px;
  image: url(:/icon/theme/{icon_dir}/primary/uparrow.svg);
  border-width: 0px;
  margin-right: 4px;
}}

QDateTimeEdit::up-button:disabled,
QDoubleSpinBox::up-button:disabled,
QSpinBox::up-button:disabled {{
  image: url(:/icon/theme/{icon_dir}/disabled/uparrow.svg);
}}

QDateTimeEdit::down-button,
QDoubleSpinBox::down-button,
QSpinBox::down-button {{
  subcontrol-origin: border;
  subcontrol-position: bottom right;
  width: 20px;
  image: url(:/icon/theme/{icon_dir}/primary/downarrow.svg);
  border-width: 0px;
  margin-right: 4px;
}}

QDateTimeEdit::down-button:disabled,
QDoubleSpinBox::down-button:disabled,
QSpinBox::down-button:disabled {{
  image: url(:/icon/theme/{icon_dir}/disabled/downarrow.svg);
}}

/* ------------------------------------------------------------------------ */
/* QPushButton                                                              */

QPushButton {{
  color: {text};
  background-color: {bg_elevated};
  border: 1px solid {border_strong};
  border-radius: 7px;
  margin: 0px;
  padding: 0px 14px;
  height: 32px;
  min-height: 32px;
  max-height: 34px;
  font-weight: 600;
}}

QPushButton:hover {{
  color: {primary};
  background-color: {bg_hover};
  border-color: {primary};
}}

QPushButton:checked,
QPushButton:pressed {{
  color: {primary_text};
  background-color: {primary};
  border-color: {primary};
}}

/* Primary accent buttons */
QPushButton[variant="primary"],
NavigationWidget QPushButton#pushButton,
CommentView QPushButton#pushButton,
AllCommentView QPushButton#pushButton,
SubCommentView QPushButton#pushButton,
MyCommentView QPushButton#pushButton,
DownloadView QPushButton#pushButton,
QPushButton#searchButton,
QPushButton#startRead,
QPushButton#readOffline,
QPushButton#loginButton,
QPushButton#downButton,
QPushButton#saveButton,
QPushButton#registerButton {{
  color: {primary_text};
  background-color: {primary};
  border: 1px solid {primary};
}}

QPushButton[variant="primary"]:hover,
NavigationWidget QPushButton#pushButton:hover,
CommentView QPushButton#pushButton:hover,
AllCommentView QPushButton#pushButton:hover,
SubCommentView QPushButton#pushButton:hover,
MyCommentView QPushButton#pushButton:hover,
DownloadView QPushButton#pushButton:hover,
QPushButton#searchButton:hover,
QPushButton#startRead:hover,
QPushButton#readOffline:hover,
QPushButton#loginButton:hover,
QPushButton#downButton:hover,
QPushButton#saveButton:hover,
QPushButton#registerButton:hover {{
  color: {primary_text};
  background-color: {primary_hover};
  border-color: {primary_hover};
}}

QPushButton[variant="primary"]:pressed,
NavigationWidget QPushButton#pushButton:pressed,
CommentView QPushButton#pushButton:pressed,
AllCommentView QPushButton#pushButton:pressed,
SubCommentView QPushButton#pushButton:pressed,
MyCommentView QPushButton#pushButton:pressed,
DownloadView QPushButton#pushButton:pressed,
QPushButton#searchButton:pressed,
QPushButton#startRead:pressed,
QPushButton#readOffline:pressed,
QPushButton#loginButton:pressed,
QPushButton#downButton:pressed,
QPushButton#saveButton:pressed,
QPushButton#registerButton:pressed {{
  color: {primary_text};
  background-color: {primary_pressed};
  border-color: {primary_pressed};
}}

/* QCommandLinkButton */
QCommandLinkButton {{
  color: {text};
  background-color: transparent;
  border: 1px solid transparent;
  border-radius: 8px;
  padding: 6px 12px;
  min-height: 32px;
  max-height: 40px;
  font-weight: 500;
  text-align: left;
}}

QCommandLinkButton:hover {{
  color: {primary};
  background-color: {primary_soft};
  border-color: transparent;
}}

QCommandLinkButton:pressed,
QCommandLinkButton:checked {{
  color: {primary};
  background-color: {primary_soft_hover};
  border-color: transparent;
  font-weight: 600;
}}

QPushButton:flat,
QPushButton#menuButton {{
  padding: 4px 10px;
  margin: 0px;
  color: {text};
  border: none;
  background-color: transparent;
}}

QPushButton:flat:hover,
QPushButton#menuButton:hover {{
  color: {primary};
  background-color: {primary_soft};
}}

QPushButton:flat:pressed,
QPushButton:flat:checked,
QPushButton#menuButton:pressed {{
  color: {primary};
  background-color: {primary_soft_hover};
}}

QPushButton:disabled,
QPushButton:flat:disabled {{
  color: {text_disabled};
  background-color: transparent;
  border: 1px solid {border};
}}

QPushButton:flat:disabled {{
  border: none;
}}

QPushButton:checked:disabled {{
  color: {text_disabled};
  background-color: {bg_hover};
  border-color: {border};
}}

/* Semantic Buttons */
QPushButton.danger {{
  border-color: {danger};
  color: {danger};
}}

QPushButton.danger:hover {{
  background-color: {danger_soft};
}}

QPushButton.danger:checked,
QPushButton.danger:pressed {{
  color: {primary_text};
  background-color: {danger};
}}

QPushButton.warning {{
  border-color: {warning};
  color: {warning};
}}

QPushButton.warning:hover {{
  background-color: {warning_soft};
}}

QPushButton.warning:checked,
QPushButton.warning:pressed {{
  color: {primary_text};
  background-color: {warning};
}}

QPushButton.success {{
  border-color: {success};
  color: {success};
}}

QPushButton.success:hover {{
  background-color: {success_soft};
}}

QPushButton.success:checked,
QPushButton.success:pressed {{
  color: {primary_text};
  background-color: {success};
}}

/* ------------------------------------------------------------------------ */
/* QTabBar                                                                  */

QTabBar {{
  font-weight: 600;
}}

QTabBar::tab {{
  color: {text_muted};
  background-color: transparent;
  border: 0px;
}}

QTabBar::tab:bottom,
QTabBar::tab:top {{
  padding: 0 16px;
  height: 34px;
}}

QTabBar::tab:left,
QTabBar::tab:right {{
  padding: 14px 0;
  width: 32px;
}}

QTabBar::tab:top:hover,
QTabBar::tab:bottom:hover,
QTabBar::tab:left:hover,
QTabBar::tab:right:hover {{
  color: {text};
}}

QTabBar::tab:top:selected {{
  color: {primary};
  border-bottom: 2px solid {primary};
}}

QTabBar::tab:bottom:selected {{
  color: {primary};
  border-top: 2px solid {primary};
}}

QTabBar::tab:right:selected {{
  color: {primary};
  border-left: 2px solid {primary};
}}

QTabBar::tab:left:selected {{
  color: {primary};
  border-right: 2px solid {primary};
}}

QTabBar QToolButton,
QTabBar QToolButton:hover {{
  border: none;
  background-color: {bg_base};
}}

QTabBar QToolButton::up-arrow {{
  image: url(:/icon/theme/{icon_dir}/disabled/uparrow2.svg);
}}
QTabBar QToolButton::up-arrow:hover {{
  image: url(:/icon/theme/{icon_dir}/primary/uparrow2.svg);
}}
QTabBar QToolButton::down-arrow {{
  image: url(:/icon/theme/{icon_dir}/disabled/downarrow2.svg);
}}
QTabBar QToolButton::down-arrow:hover {{
  image: url(:/icon/theme/{icon_dir}/primary/downarrow2.svg);
}}
QTabBar QToolButton::right-arrow {{
  image: url(:/icon/theme/{icon_dir}/disabled/rightarrow2.svg);
}}
QTabBar QToolButton::right-arrow:hover {{
  image: url(:/icon/theme/{icon_dir}/primary/rightarrow2.svg);
}}
QTabBar QToolButton::left-arrow {{
  image: url(:/icon/theme/{icon_dir}/disabled/leftarrow2.svg);
}}
QTabBar QToolButton::left-arrow:hover {{
  image: url(:/icon/theme/{icon_dir}/primary/leftarrow2.svg);
}}
QTabBar::close-button {{
  image: url(:/icon/theme/{icon_dir}/disabled/tab_close.svg);
}}
QTabBar::close-button:hover {{
  image: url(:/icon/theme/{icon_dir}/primary/tab_close.svg);
}}

/* ------------------------------------------------------------------------ */
/* QGroupBox                                                                */

QGroupBox {{
  background-color: {bg_surface};
  border: 1px solid {border};
  border-radius: 8px;
  padding: 14px;
  padding-top: 28px;
  margin-top: 6px;
}}

QGroupBox::title {{
  color: {text_muted};
  font-weight: 600;
  subcontrol-origin: margin;
  subcontrol-position: top left;
  padding: 0 12px;
  margin-top: 8px;
  background-color: transparent;
  height: 20px;
}}

/* ------------------------------------------------------------------------ */
/* QRadioButton & QCheckBox                                                 */

QRadioButton,
QCheckBox {{
  spacing: 8px;
  color: {text};
  height: 28px;
  background-color: transparent;
}}

QRadioButton:disabled,
QCheckBox:disabled {{
  color: {text_disabled};
}}

QGroupBox::indicator {{
  width: 18px;
  height: 18px;
  border-radius: 4px;
}}

QMenu::indicator,
QListView::indicator,
QTableWidget::indicator,
QRadioButton::indicator,
QCheckBox::indicator {{
  width: 22px;
  height: 22px;
  border-radius: 4px;
}}

QListView::indicator:checked,
QListView::indicator:checked:selected,
QListView::indicator:checked:focus {{
  image: url(:/icon/theme/{icon_dir}/primary/checklist.svg);
}}
QListView::indicator:checked:selected:active {{
  image: url(:/icon/theme/{icon_dir}/primary/checklist_invert.svg);
}}
QListView::indicator:checked:disabled {{
  image: url(:/icon/theme/{icon_dir}/disabled/checklist.svg);
}}
QListView::indicator:indeterminate,
QListView::indicator:indeterminate:selected,
QListView::indicator:indeterminate:focus {{
  image: url(:/icon/theme/{icon_dir}/primary/checklist_indeterminate.svg);
}}
QListView::indicator:indeterminate:selected:active {{
  image: url(:/icon/theme/{icon_dir}/primary/checklist_indeterminate_invert.svg);
}}
QListView::indicator:indeterminate:disabled {{
  image: url(:/icon/theme/{icon_dir}/disabled/checklist_indeterminate.svg);
}}

QTableView::indicator:enabled:checked,
QTableView::indicator:enabled:checked:selected,
QTableView::indicator:enabled:checked:focus {{
  image: url(:/icon/theme/{icon_dir}/primary/checkbox_checked.svg);
}}
QTableView::indicator:checked:selected:active {{
  image: url(:/icon/theme/{icon_dir}/primary/checkbox_checked_invert.svg);
}}
QTableView::indicator:disabled:checked,
QTableView::indicator:disabled:checked:selected,
QTableView::indicator:disabled:checked:focus {{
  image: url(:/icon/theme/{icon_dir}/disabled/checkbox_checked.svg);
}}
QTableView::indicator:enabled:unchecked,
QTableView::indicator:enabled:unchecked:selected,
QTableView::indicator:enabled:unchecked:focus {{
  image: url(:/icon/theme/{icon_dir}/primary/checkbox_unchecked.svg);
}}
QTableView::indicator:unchecked:selected:active {{
  image: url(:/icon/theme/{icon_dir}/primary/checkbox_unchecked_invert.svg);
}}
QTableView::indicator:disabled:unchecked,
QTableView::indicator:disabled:unchecked:selected,
QTableView::indicator:disabled:unchecked:focus {{
  image: url(:/icon/theme/{icon_dir}/disabled/checkbox_unchecked.svg);
}}
QTableView::indicator:enabled:indeterminate,
QTableView::indicator:enabled:indeterminate:selected,
QTableView::indicator:enabled:indeterminate:focus {{
  image: url(:/icon/theme/{icon_dir}/primary/checkbox_indeterminate.svg);
}}
QTableView::indicator:indeterminate:selected:active {{
  image: url(:/icon/theme/{icon_dir}/primary/checkbox_indeterminate_invert.svg);
}}
QTableView::indicator:disabled:indeterminate,
QTableView::indicator:disabled:indeterminate:selected,
QTableView::indicator:disabled:indeterminate:focus {{
  image: url(:/icon/theme/{icon_dir}/disabled/checkbox_indeterminate.svg);
}}

QCheckBox::indicator:checked,
QGroupBox::indicator:checked {{
  image: url(:/icon/theme/{icon_dir}/primary/checkbox_checked.svg);
}}
QCheckBox::indicator:unchecked,
QGroupBox::indicator:unchecked {{
  image: url(:/icon/theme/{icon_dir}/primary/checkbox_unchecked.svg);
}}
QCheckBox::indicator:indeterminate,
QGroupBox::indicator:indeterminate {{
  image: url(:/icon/theme/{icon_dir}/primary/checkbox_indeterminate.svg);
}}
QCheckBox::indicator:checked:disabled,
QGroupBox::indicator:checked:disabled {{
  image: url(:/icon/theme/{icon_dir}/disabled/checkbox_checked.svg);
}}
QCheckBox::indicator:unchecked:disabled,
QGroupBox::indicator:unchecked:disabled {{
  image: url(:/icon/theme/{icon_dir}/disabled/checkbox_unchecked.svg);
}}
QCheckBox::indicator:indeterminate:disabled,
QGroupBox::indicator:indeterminate:disabled {{
  image: url(:/icon/theme/{icon_dir}/disabled/checkbox_indeterminate.svg);
}}

QRadioButton::indicator:checked {{
  image: url(:/icon/theme/{icon_dir}/primary/radiobutton_checked.svg);
}}
QRadioButton::indicator:unchecked {{
  image: url(:/icon/theme/{icon_dir}/primary/radiobutton_unchecked.svg);
}}
QRadioButton::indicator:checked:disabled {{
  image: url(:/icon/theme/{icon_dir}/disabled/radiobutton_checked.svg);
}}
QRadioButton::indicator:unchecked:disabled {{
  image: url(:/icon/theme/{icon_dir}/disabled/radiobutton_unchecked.svg);
}}

/* ------------------------------------------------------------------------ */
/* QDockWidget                                                              */

QDockWidget {{
  color: {text};
  border: 1px solid {border};
  titlebar-close-icon: url(:/icon/theme/{icon_dir}/primary/close.svg);
  titlebar-normal-icon: url(:/icon/theme/{icon_dir}/primary/float.svg);
  border-radius: 8px;
}}

QDockWidget::title {{
  text-align: left;
  padding-left: 16px;
  padding-top: 6px;
  padding-bottom: 6px;
}}

/* ------------------------------------------------------------------------ */
/* Menus & ComboBox Items                                                   */

QComboBox::indicator:checked {{
  image: url(:/icon/theme/{icon_dir}/primary/checklist.svg);
}}
QComboBox::indicator:checked:selected {{
  image: url(:/icon/theme/{icon_dir}/primary/checklist_invert.svg);
}}

QComboBox::item,
QCalendarWidget QMenu::item,
QMenu::item {{
  height: 28px;
  border: 4px solid transparent;
  color: {text};
  border-radius: 6px;
}}

QCalendarWidget QMenu::item,
QMenu::item {{
  padding: 4px 20px 4px 14px;
}}

QComboBox::item:selected,
QCalendarWidget QMenu::item:selected,
QMenu::item:selected {{
  color: {primary};
  background-color: {primary_soft};
  border-radius: 6px;
}}

QComboBox::item:disabled,
QCalendarWidget QMenu::item:disabled,
QMenu::item:disabled {{
  color: {text_disabled};
}}

QCalendarWidget QMenu,
QMenu {{
  background-color: {bg_elevated};
  border: 1px solid {border_strong};
  border-radius: 8px;
  padding: 4px;
}}

QMenu::separator {{
  height: 1px;
  background-color: {divider};
  margin: 4px 8px;
}}

QMenu::right-arrow {{
  image: url(:/icon/theme/{icon_dir}/primary/rightarrow.svg);
  width: 14px;
  height: 14px;
}}
QMenu::right-arrow:selected {{
  image: url(:/icon/theme/{icon_dir}/disabled/rightarrow.svg);
}}
QMenu::indicator:non-exclusive:unchecked {{
  image: url(:/icon/theme/{icon_dir}/primary/checkbox_unchecked.svg);
}}
QMenu::indicator:non-exclusive:unchecked:selected {{
  image: url(:/icon/theme/{icon_dir}/primary/checkbox_unchecked_invert.svg);
}}
QMenu::indicator:non-exclusive:checked {{
  image: url(:/icon/theme/{icon_dir}/primary/checkbox_checked.svg);
}}
QMenu::indicator:non-exclusive:checked:selected {{
  image: url(:/icon/theme/{icon_dir}/primary/checkbox_checked_invert.svg);
}}
QMenu::indicator:exclusive:unchecked {{
  image: url(:/icon/theme/{icon_dir}/primary/radiobutton_unchecked.svg);
}}
QMenu::indicator:exclusive:unchecked:selected {{
  image: url(:/icon/theme/{icon_dir}/primary/radiobutton_unchecked_invert.svg);
}}
QMenu::indicator:exclusive:checked {{
  image: url(:/icon/theme/{icon_dir}/primary/radiobutton_checked.svg);
}}
QMenu::indicator:exclusive:checked:selected {{
  image: url(:/icon/theme/{icon_dir}/primary/radiobutton_checked_invert.svg);
}}

/* ------------------------------------------------------------------------ */
/* QMenuBar & QToolBox                                                      */

QMenuBar {{
  background-color: {bg_surface};
  color: {text};
  border-bottom: 1px solid {divider};
}}

QMenuBar::item {{
  height: 30px;
  padding: 6px 10px;
  background-color: transparent;
  color: {text};
  border-radius: 6px;
}}

QMenuBar::item:selected,
QMenuBar::item:pressed {{
  color: {primary};
  background-color: {primary_soft};
}}

QToolBox::tab {{
  background-color: {bg_surface};
  color: {text};
  border-radius: 6px;
  padding-left: 10px;
}}

QToolBox::tab:selected,
QToolBox::tab:hover {{
  color: {primary};
  background-color: {primary_soft};
}}

/* ------------------------------------------------------------------------ */
/* QProgressBar                                                             */

QProgressBar {{
  border: none;
  border-radius: 4px;
  background-color: {progress_bg};
  text-align: center;
  color: transparent;
  min-height: 8px;
}}

QProgressBar::chunk {{
  background-color: {primary};
  border-radius: 4px;
}}

/* ------------------------------------------------------------------------ */
/* Modern Capsule QScrollBar                                                */

QScrollBar:vertical {{
  border: none;
  background: transparent;
  width: 8px;
  margin: 2px 0px 2px 0px;
}}

QScrollBar:horizontal {{
  border: none;
  background: transparent;
  height: 8px;
  margin: 0px 2px 0px 2px;
}}

QScrollBar::handle:vertical {{
  background: {scroll_handle};
  min-height: 32px;
  border-radius: 4px;
}}

QScrollBar::handle:horizontal {{
  background: {scroll_handle};
  min-width: 32px;
  border-radius: 4px;
}}

QScrollBar::handle:vertical:hover,
QScrollBar::handle:horizontal:hover {{
  background: {scroll_handle_hover};
}}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical,
QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {{
  background: none;
}}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{
  height: 0px;
  width: 0px;
  background: none;
  border: none;
}}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {{
  height: 0px;
  width: 0px;
  background: none;
  border: none;
}}

QScrollBar::up-arrow:vertical,
QScrollBar::down-arrow:vertical,
QScrollBar::left-arrow:horizontal,
QScrollBar::right-arrow:horizontal {{
  width: 0px;
  height: 0px;
  background: none;
}}

/* ------------------------------------------------------------------------ */
/* QSlider                                                                  */

QSlider:horizontal {{
  min-height: 22px;
  max-height: 22px;
}}

QSlider:vertical {{
  min-width: 22px;
  max-width: 22px;
}}

QSlider::groove:horizontal {{
  height: 4px;
  background: {slider_groove};
  border-radius: 2px;
  margin: 0 8px;
}}

QSlider::groove:vertical {{
  width: 4px;
  background: {slider_groove};
  border-radius: 2px;
  margin: 8px 0;
}}

QSlider::handle:horizontal {{
  image: url(:/icon/theme/{icon_dir}/primary/slider.svg);
  width: 18px;
  height: 18px;
  margin: -7px -9px;
}}

QSlider::handle:vertical {{
  image: url(:/icon/theme/{icon_dir}/primary/slider.svg);
  border-radius: 9px;
  width: 18px;
  height: 18px;
  margin: -9px -7px;
}}

QSlider::add-page {{
  background: {slider_groove};
  border-radius: 2px;
}}

QSlider::sub-page {{
  background: {primary};
  border-radius: 2px;
}}

/* ------------------------------------------------------------------------ */
/* QLabel & Dividers                                                        */

QLabel {{
  border: none;
  background: transparent;
  color: {text};
}}

QLabel:disabled {{
  color: {text_disabled};
}}

QFrame[frameShape="4"] {{
  border-width: 1px 0 0 0;
  background: none;
}}

QFrame[frameShape="5"] {{
  border-width: 0 1px 0 0;
  background: none;
}}

QFrame[frameShape="4"],
QFrame[frameShape="5"] {{
  border-color: {divider};
}}

/* ------------------------------------------------------------------------ */
/* QToolBar & QToolButton                                                   */

QToolBar {{
  background: {bg_surface};
  border: none;
}}

QToolBar:horizontal {{
  border-bottom: 1px solid {divider};
}}

QToolBar:vertical {{
  border-right: 1px solid {divider};
}}

QToolBar::handle:horizontal {{
  image: url(:/icon/theme/{icon_dir}/primary/toolbar-handle-horizontal.svg);
}}

QToolBar::handle:vertical {{
  image: url(:/icon/theme/{icon_dir}/primary/toolbar-handle-vertical.svg);
}}

QToolBar::separator:horizontal {{
  border-right: 1px solid {divider};
  width: 1px;
}}

QToolBar::separator:vertical {{
  border-top: 1px solid {divider};
  height: 1px;
}}

QToolButton {{
  background-color: transparent;
  color: {text};
  border: none;
  border-radius: 7px;
  height: 28px;
  margin: 1px 2px;
  padding: 2px 10px;
}}

QToolButton:hover {{
  background-color: {bg_hover};
}}

QToolButton:pressed {{
  background-color: {bg_pressed};
}}

QToolButton:checked {{
  background-color: {primary_soft};
  color: {primary};
  font-weight: 600;
}}

QToolButton:checked:hover {{
  background-color: {primary_soft_hover};
}}

/* ------------------------------------------------------------------------ */
/* Tables, Trees & Lists                                                    */

QTableView {{
  background-color: {bg_surface};
  alternate-background-color: {bg_alt};
  border: 1px solid {border};
  border-radius: 8px;
  gridline-color: {divider};
  selection-background-color: {primary_soft};
  selection-color: {text};
}}

QTreeView,
QListView {{
  border-radius: 8px;
  padding: 4px;
  margin: 0px;
}}

QTableView::item,
QTreeView::item,
QListView::item {{
  padding: 6px 8px;
  min-height: 26px;
  color: {text};
  selection-color: {text};
  border-color: transparent;
}}

QTableView::item:hover,
QTreeView::item:hover,
QListView::item:hover {{
  background-color: {bg_hover};
  border-radius: 6px;
}}

QTableView::item:selected,
QTreeView::item:selected,
QListView::item:selected {{
  background-color: {primary_soft};
  selection-background-color: {primary_soft};
  color: {primary};
  selection-color: {primary};
  border-radius: 6px;
}}

QTableView::item:selected:focus,
QTreeView::item:selected:focus,
QListView::item:selected:focus {{
  background-color: {primary_soft_hover};
  selection-background-color: {primary_soft_hover};
  color: {primary};
  selection-color: {primary};
}}

QTableView::item:disabled {{
  color: {text_disabled};
  background-color: {bg_alt};
}}

/* Specialized list item overrides (must come after generic QListView::item) */
ComicListWidget::item,
ComicListWidget::item:hover,
ComicListWidget::item:selected,
ComicListWidget::item:selected:focus {{
  background-color: transparent;
  border: none;
  padding: 0px;
  margin: 0px;
}}

UserListWidget::item {{
  border-bottom: 1px solid {divider};
  padding: 6px 4px;
}}

UserListWidget::item:hover,
UserListWidget::item:selected,
UserListWidget::item:selected:focus {{
  background-color: transparent;
}}

NasView QListWidget::item {{
  background-color: {bg_surface};
  border: 1px solid {border};
  border-radius: 8px;
  margin: 4px 2px;
}}

NasView QListWidget::item:hover {{
  border-color: {border_strong};
  background-color: {bg_hover};
}}

QTreeView::branch {{
  background-color: transparent;
}}
QTreeView::branch:closed:has-children:has-siblings,
QTreeView::branch:closed:has-children:!has-siblings {{
  image: url(:/icon/theme/{icon_dir}/primary/branch-closed.svg);
}}
QTreeView::branch:open:has-children:!has-siblings,
QTreeView::branch:open:has-children:has-siblings {{
  image: url(:/icon/theme/{icon_dir}/primary/branch-open.svg);
}}
QTreeView::branch:has-siblings:!adjoins-item {{
  border-image: url(:/icon/theme/{icon_dir}/disabled/vline.svg) 0;
}}
QTreeView::branch:has-siblings:adjoins-item {{
  border-image: url(:/icon/theme/{icon_dir}/disabled/branch-more.svg) 0;
}}
QTreeView::branch:!has-children:!has-siblings:adjoins-item,
QTreeView::branch:has-children:!has-siblings:adjoins-item {{
  border-image: url(:/icon/theme/{icon_dir}/disabled/branch-end.svg) 0;
}}

QTableCornerButton::section {{
  background-color: {bg_surface};
  border: none;
  border-bottom: 1px solid {divider};
}}

QHeaderView {{
  border: none;
  background-color: transparent;
}}

QHeaderView::section {{
  color: {text_muted};
  font-weight: 600;
  background-color: {bg_surface};
  padding: 0 14px;
  height: 36px;
  border: none;
  border-bottom: 1px solid {divider};
}}

QTreeView QHeaderView::section {{
  border: none;
}}

/* ------------------------------------------------------------------------ */
/* Misc Widgets                                                             */

QLCDNumber {{
  color: {primary};
  background-color: {primary_soft};
  border: 1px solid {primary_border_soft};
  border-radius: 6px;
}}

#qt_calendar_prevmonth {{
  qproperty-icon: url(:/icon/theme/{icon_dir}/primary/leftarrow.svg);
}}

#qt_calendar_nextmonth {{
  qproperty-icon: url(:/icon/theme/{icon_dir}/primary/rightarrow.svg);
}}

QTreeView QLineEdit,
QTableView QLineEdit,
QListView QLineEdit {{
  color: {text};
  background-color: {bg_elevated};
  border: 1px solid {primary};
  border-radius: 4px;
  padding: 2px 6px;
}}
"""


def build_all():
    for name, tokens in THEMES.items():
        qss = QSS_TEMPLATE.format(name=name, **tokens)
        out_path = THEME_DIR / f"{name}.qss"
        out_path.write_text(qss, encoding="utf-8", newline="\n")
        print(f"Generated {out_path} ({len(qss)} bytes)")


if __name__ == "__main__":
    build_all()
