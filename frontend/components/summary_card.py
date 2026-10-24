from PyQt5.QtWidgets import (
    QFrame,
    QLabel,
    QWidget,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QVBoxLayout,
)
from PyQt5.QtGui import QColor

from components.style_constants import (
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED,
    FONT_FAMILY,
    COLOR_BORDER,
)

WARNING_BG = "#FFF4E5"
WARNING_TEXT = "#D17000"

class StatItem(QWidget):
    def __init__(self, label="", value="", parent=None):
        super().__init__(parent)

        self._label = QLabel(str(label))
        self._label.setObjectName("stat_label")
        self._value = QLabel(str(value))
        self._value.setObjectName("stat_value")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        layout.addWidget(self._label)
        layout.addWidget(self._value)

        self.setStyleSheet(f"""
            QLabel#stat_label{{
                font-family: {FONT_FAMILY};
                color: {COLOR_TEXT_MUTED};
                font-size: 13px;
            }}
            QLabel#stat_value{{
                font-family: {FONT_FAMILY};
                color: {COLOR_TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 600;
            }}
        """)

    def set_label(self, text):
        self._label.setText(str(text))

    def set_value(self, text):
        self._value.setText(str(text))

    def set_stat(self, label=None, value=None):
        if label is not None:
            self.set_label(label)
        if value is not None:
            self.set_value(value)


class HighlightBox(QFrame):
    def __init__(
        self,
        label="",
        value="",
        bg_color=WARNING_BG,
        text_color=WARNING_TEXT,
        parent=None,
    ):
        super().__init__(parent)
        self.setObjectName("highlight_box")

        self._label = QLabel(str(label))
        self._label.setObjectName("highlight_label")
        self._value = QLabel(str(value))
        self._value.setObjectName("highlight_value")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(2)
        layout.addWidget(self._label)
        layout.addWidget(self._value)

        self.set_colors(bg_color, text_color)

    def set_label(self, text):
        self._label.setText(str(text))

    def set_value(self, text):
        self._value.setText(str(text))

    def set_stat(self, label=None, value=None):
        if label is not None:
            self.set_label(label)
        if value is not None:
            self.set_value(value)

    def set_colors(self, bg_color, text_color):
        self.setStyleSheet(f"""
            QFrame#highlight_box{{
                background-color: {bg_color};
                border: none;
                border-radius: 8px;
            }}
            QLabel#highlight_label{{
                font-family: {FONT_FAMILY};
                color: {text_color};
                font-size: 13px;
            }}
            QLabel#highlight_value{{
                font-family: {FONT_FAMILY};
                color: {text_color};
                font-size: 16px;
                font-weight: 600;
            }}
        """)

class SummaryCard(QFrame):

    def __init__(
        self,
        title,
        top_left,
        bottom_left,
        top_right,
        highlight,
        highlight_bg=WARNING_BG,
        highlight_text=WARNING_TEXT,
        parent=None,
    ):
        super().__init__(parent)
        self.setObjectName("summary_card_outer")

        self._build_ui(
            title, top_left, bottom_left, top_right, highlight,
            highlight_bg, highlight_text,
        )
        self._apply_style()
        self._apply_shadow()

    def _build_ui(self, title, top_left, bottom_left, top_right, highlight,
                  highlight_bg, highlight_text):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(14, 14, 14, 18)

        self.card = QFrame()
        self.card.setObjectName("summary_card")
        outer_layout.addWidget(self.card)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(22, 18, 22, 20)
        card_layout.setSpacing(16)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("card_title")

        self.top_left = StatItem(*top_left)
        self.bottom_left = StatItem(*bottom_left)
        self.top_right = StatItem(*top_right)
        self.highlight = HighlightBox(
            *highlight, bg_color=highlight_bg, text_color=highlight_text
        )

        left_column = QVBoxLayout()
        left_column.setSpacing(18)
        left_column.addWidget(self.top_left)
        left_column.addWidget(self.bottom_left)
        left_column.addStretch()

        right_column = QVBoxLayout()
        right_column.setSpacing(12)
        right_column.addWidget(self.top_right)
        right_column.addWidget(self.highlight)
        right_column.addStretch()

        divider = QFrame()
        divider.setObjectName("card_divider")
        divider.setFrameShape(QFrame.VLine)
        divider.setFixedWidth(1)

        body = QHBoxLayout()
        body.setSpacing(24)
        body.addLayout(left_column, stretch=1)
        body.addWidget(divider)
        body.addLayout(right_column, stretch=1)

        card_layout.addWidget(self.title_label)
        card_layout.addLayout(body)

    def _apply_style(self):
        self.setStyleSheet(f"""
            QFrame#summary_card_outer{{
                background: transparent;
                border: none;
            }}
            QFrame#summary_card{{
                background-color: #FFFFFF;
                border: 1px solid {COLOR_BORDER};
                border-radius: 14px;
            }}
            QLabel#card_title{{
                font-family: {FONT_FAMILY};
                color: {COLOR_TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 600;
            }}
            QFrame#card_divider{{
                background-color: {COLOR_BORDER};
                border: none;
            }}
        """)

    def _apply_shadow(self):
        shadow = QGraphicsDropShadowEffect(self.card)
        shadow.setBlurRadius(28)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(16, 24, 40, 28))
        self.card.setGraphicsEffect(shadow)

    def set_title(self, text):
        self.title_label.setText(str(text))
