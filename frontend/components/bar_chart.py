import math

from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QWidget,
    QLabel,
    QSizePolicy,
    QToolTip,
    QHBoxLayout,
    QVBoxLayout,
)
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QPainterPath

from components.style_constants import (
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED,
    FONT_FAMILY,
    COLOR_BORDER,
)

DEFAULT_BAR_COLOR = "#0F9D6B"      # green (actual values)
DEFAULT_TARGET_COLOR = "#D9DDE3"   # grey (targets)
GRID_COLOR = "#E5E7EB"


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def format_short(value):
    """150000 -> '150K', 2500000 -> '2.5M', 0 -> '0'."""
    if value >= 1_000_000:
        return f"{value / 1_000_000:g}M"
    if value >= 1_000:
        return f"{value / 1_000:g}K"
    return f"{value:g}"


def nice_scale(max_value, target_steps=3):
    """Return (step, top) so the axis ends on a round number (e.g. 50K, 150K)."""
    if max_value <= 0:
        return 1, 1
    rough = max_value / target_steps
    magnitude = 10 ** math.floor(math.log10(rough))
    residual = rough / magnitude
    if residual <= 1:
        nice = 1
    elif residual <= 2:
        nice = 2
    elif residual <= 5:
        nice = 5
    else:
        nice = 10
    step = nice * magnitude
    top = math.ceil(max_value / step) * step
    return step, top

class BarChartCanvas(QWidget):
    def __init__(
        self,
        bar_color=DEFAULT_BAR_COLOR,
        target_color=DEFAULT_TARGET_COLOR,
        tooltip_prefix="",
        parent=None,
    ):
        super().__init__(parent)
        self.bar_color = QColor(bar_color)
        self.target_color = QColor(target_color)
        self.tooltip_prefix = tooltip_prefix

        self._labels = []
        self._values = []
        self._targets = []

        self._plot = QRectF()
        self._top = 1

        self.setMinimumHeight(220)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMouseTracking(True)

    def set_data(self, labels, values, targets=None):
        n = len(labels)
        self._labels = list(labels)
        self._values = list(values) + [None] * (n - len(values))
        self._targets = (list(targets) if targets else []) + [None] * (
            n - len(targets or [])
        )
        self.update()

    def _bar_info(self, i):
        value = self._values[i]
        if value is not None:
            return value, False
        target = self._targets[i]
        if target is not None:
            return target, True
        return None, False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        n = len(self._labels)
        font = QFont(FONT_FAMILY.split(",")[0].strip("'\" "))
        font.setPixelSize(12)
        painter.setFont(font)
        fm = painter.fontMetrics()

        heights = [self._bar_info(i)[0] for i in range(n)]
        max_value = max([v for v in heights if v is not None] or [0])
        step, top = nice_scale(max_value)
        self._top = top
        ticks = [step * k for k in range(int(round(top / step)) + 1)]

        left = max(fm.horizontalAdvance(format_short(t)) for t in ticks) + 14
        bottom = fm.height() + 12
        plot = QRectF(left, 10, self.width() - left - 10, self.height() - 10 - bottom)
        self._plot = plot

        grid_pen = QPen(QColor(GRID_COLOR))
        grid_pen.setWidth(1)
        for t in ticks:
            y = plot.bottom() - (t / top) * plot.height()
            painter.setPen(grid_pen)
            painter.drawLine(int(plot.left()), int(y), int(plot.right()), int(y))

            painter.setPen(QColor(COLOR_TEXT_MUTED))
            painter.drawText(
                QRectF(0, y - fm.height() / 2, left - 8, fm.height()),
                Qt.AlignRight | Qt.AlignVCenter,
                format_short(t),
            )

        if n == 0:
            return

        slot = plot.width() / n
        bar_w = min(slot * 0.45, 26)
        radius = 3

        for i in range(n):
            x = plot.left() + slot * i + (slot - bar_w) / 2

            value, is_target = self._bar_info(i)
            if value is not None:
                y = plot.bottom() - (value / top) * plot.height()
                h = plot.bottom() - y

                painter.save()
                painter.setClipRect(QRectF(plot.left() - 1, 0, plot.width() + 2, plot.bottom()))
                path = QPainterPath()
                path.addRoundedRect(QRectF(x, y, bar_w, h + radius * 2), radius, radius)
                painter.fillPath(path, self.target_color if is_target else self.bar_color)
                painter.restore()

            painter.setPen(QColor(COLOR_TEXT_MUTED))
            painter.drawText(
                QRectF(plot.left() + slot * i, plot.bottom() + 6, slot, fm.height()),
                Qt.AlignHCenter | Qt.AlignVCenter,
                str(self._labels[i]),
            )

    def mouseMoveEvent(self, event):
        n = len(self._labels)
        if n and self._plot.contains(event.x(), event.y()):
            i = int((event.x() - self._plot.left()) / (self._plot.width() / n))
            i = max(0, min(n - 1, i))
            value, is_target = self._bar_info(i)
            if value is not None:
                kind = "Target" if is_target else "Actual"
                QToolTip.showText(
                    event.globalPos(),
                    f"{self._labels[i]} - {kind}: {self.tooltip_prefix}{value:,.0f}",
                    self,
                )
                return
        QToolTip.hideText()

class TrendBarChart(QFrame):
    def __init__(
        self,
        title="Contribution Trend",
        series_name="Contributions",
        target_name="Target",
        bar_color=DEFAULT_BAR_COLOR,
        target_color=DEFAULT_TARGET_COLOR,
        tooltip_prefix="KES ",
        parent=None,
    ):
        super().__init__(parent)
        self.setObjectName("chart_card")

        self.chart = BarChartCanvas(
            bar_color=bar_color,
            target_color=target_color,
            tooltip_prefix=tooltip_prefix,
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 12)
        layout.setSpacing(8)

        header_row = QHBoxLayout()
        header_row.setSpacing(12)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("chart_title")

        header_row.addWidget(self.title_label)
        header_row.addStretch()
        header_row.addLayout(self._legend_item(series_name, bar_color))

        separator = QFrame()
        separator.setObjectName("chart_separator")
        separator.setFixedSize(1, 14)
        header_row.addWidget(separator, alignment=Qt.AlignVCenter)

        header_row.addLayout(self._legend_item(target_name, target_color))

        layout.addLayout(header_row)
        layout.addWidget(self.chart, stretch=1)

        self.setStyleSheet(f"""
            QFrame#chart_card{{
                background-color: #FFFFFF;
                border: 1px solid {COLOR_BORDER};
                border-radius: 10px;
            }}
            QLabel#chart_title{{
                font-family: {FONT_FAMILY};
                font-size: 14px;
                font-weight: 600;
                color: {COLOR_TEXT_PRIMARY};
            }}
            QLabel#legend_text{{
                font-family: {FONT_FAMILY};
                font-size: 14px;
                color: {COLOR_TEXT_MUTED};
            }}
            QFrame#chart_separator{{
                background-color: {COLOR_BORDER};
                border: none;
            }}
        """)

    def _legend_item(self, text, color):
        row = QHBoxLayout()
        row.setSpacing(6)

        swatch = QLabel()
        swatch.setFixedSize(18, 8)
        swatch.setStyleSheet(f"background-color: {color}; border-radius: 3px;")

        label = QLabel(text)
        label.setObjectName("legend_text")

        row.addWidget(swatch, alignment=Qt.AlignVCenter)
        row.addWidget(label, alignment=Qt.AlignVCenter)
        return row

    def set_data(self, labels, values, targets=None):
        self.chart.set_data(labels, values, targets)

    def set_title(self, title):
        self.title_label.setText(title)
