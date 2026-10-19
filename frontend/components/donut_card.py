import math
from typing import Iterable, Sequence, Tuple

from PyQt5.QtCore import Qt, QRectF, QSize
from PyQt5.QtGui import QColor, QFont, QPainter, QPen
from PyQt5.QtWidgets import (
    QBoxLayout,
    QFrame,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QLabel,
    QSizePolicy,
    QToolTip,
    QVBoxLayout,
    QWidget,
)

Item = Tuple[str, float, str]

DEFAULT_DATA = [
    ("Draft",         5, "#7CB4F5"),
    ("Onboarding",    8, "#2F5BEA"),
    ("Configuration", 6, "#3ECF9A"),
    ("Review",        3, "#2BB5D8"),
    ("Activation",    2, "#F5B82E"),
]


class DonutChart(QWidget):
    def __init__(self, data: Sequence[Item] = (), center_caption: str = "",
                 center_value=None, thickness: float = 0.14, parent=None):
        super().__init__(parent)
        self._data = list(data)
        self._caption = center_caption
        self._center_value = center_value
        self._thickness = thickness
        self._value_color = QColor("#1B2559")
        self._caption_color = QColor("#6B7280")
        self._hover = -1
        self.setMouseTracking(True)
        self.setMinimumSize(120, 120)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def set_data(self, data: Iterable[Item]):
        self._data = list(data)
        self._hover = -1
        self.update()

    def set_center(self, caption: str = None, value=None):
        if caption is not None:
            self._caption = caption
        self._center_value = value
        self.update()

    def total(self):
        return sum(v for _, v, _ in self._data)

    def sizeHint(self):
        return QSize(180, 180)

    def _geometry(self):
        side = min(self.width(), self.height())
        ring = side * self._thickness
        margin = ring / 2 + 4
        rect = QRectF((self.width() - side) / 2 + margin,
                      (self.height() - side) / 2 + margin,
                      side - 2 * margin, side - 2 * margin)
        return rect, ring

    def _segment_at(self, pos):
        total = self.total()
        if total <= 0:
            return -1
        rect, ring = self._geometry()
        c = rect.center()
        dx, dy = pos.x() - c.x(), pos.y() - c.y()
        radius = rect.width() / 2
        if not (radius - ring / 2 <= math.hypot(dx, dy) <= radius + ring / 2):
            return -1
        angle = math.degrees(math.atan2(dx, -dy)) % 360
        acc = 0.0
        for i, (_, value, _) in enumerate(self._data):
            if value <= 0:
                continue
            acc += value / total * 360
            if angle < acc:
                return i
        return -1

    def mouseMoveEvent(self, event):
        idx = self._segment_at(event.pos())
        if idx != self._hover:
            self._hover = idx
            self.update()
        if idx >= 0:
            label, value, _ = self._data[idx]
            pct = round(value / (self.total() or 1) * 100)
            QToolTip.showText(event.globalPos(), f"{label}: {value:g} ({pct}%)", self)
        else:
            QToolTip.hideText()

    def leaveEvent(self, event):
        if self._hover != -1:
            self._hover = -1
            self.update()
        super().leaveEvent(event)

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        rect, ring = self._geometry()
        total = self.total()

        if total <= 0:
            pen = QPen(QColor("#E5E7EB"), ring)
            pen.setCapStyle(Qt.FlatCap)
            p.setPen(pen)
            p.drawEllipse(rect)
        else:
            start = 90 * 16
            for i, (_, value, color) in enumerate(self._data):
                if value <= 0:
                    continue
                span = -int(round(value / total * 360 * 16))
                width = ring + (6 if i == self._hover else 0)
                pen = QPen(QColor(color), width)
                pen.setCapStyle(Qt.FlatCap)
                p.setPen(pen)
                p.drawArc(rect, start, span)
                start += span

        if 0 <= self._hover < len(self._data):
            label, value, _ = self._data[self._hover]
            value_text, caption = f"{value:g}", label
        else:
            if self._center_value is not None:
                value_text = str(self._center_value)
            else:
                value_text = f"{total:g}"
            caption = self._caption

        inner = rect.adjusted(ring / 2, ring / 2, -ring / 2, -ring / 2)

        vfont = QFont(self.font())
        vfont.setBold(True)
        vfont.setPixelSize(max(14, int(inner.height() * 0.30)))
        p.setFont(vfont)
        vh = p.fontMetrics().height()

        cfont = QFont(self.font())
        cfont.setPixelSize(max(9, int(inner.height() * 0.11)))
        p.setFont(cfont)
        line_h = p.fontMetrics().height()
        cap_lines = caption.split("\n") if caption else []

        block_h = vh + line_h * len(cap_lines)
        top = inner.center().y() - block_h / 2

        p.setFont(vfont)
        p.setPen(self._value_color)
        p.drawText(QRectF(inner.left(), top, inner.width(), vh),
                   Qt.AlignHCenter | Qt.AlignVCenter, value_text)

        p.setFont(cfont)
        p.setPen(self._caption_color)
        for i, line in enumerate(cap_lines):
            p.drawText(QRectF(inner.left(), top + vh + i * line_h,
                              inner.width(), line_h),
                       Qt.AlignHCenter | Qt.AlignVCenter, line)
        p.end()


class _LegendDot(QWidget):
    def __init__(self, color: str, parent=None):
        super().__init__(parent)
        self._color = QColor(color)
        self.setFixedSize(10, 10)

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)
        p.setBrush(self._color)
        p.drawEllipse(self.rect())
        p.end()


class DonutChartCard(QFrame):
    STACK_BELOW = 380 

    def __init__(self, title: str = "", data: Sequence[Item] = DEFAULT_DATA,
                 center_caption: str = "", center_value=None,
                 show_percent: bool = True, shadow: bool = False,
                 framed: bool = True, parent=None):
        super().__init__(parent)
        self.setObjectName("donutCard")

        frame_css = (
            "background: #FFFFFF; border: 1px solid #E8ECF4; border-radius: 16px;"
            if framed else
            "background: transparent; border: none;"
        )
        self.setStyleSheet(f"""
            #donutCard {{ {frame_css} }}
            #donutCardTitle {{ color: #1B2559; font-size: 16px; font-weight: 600;
                               background: transparent; border: none; }}
            #donutLegendLabel {{ color: #1B2559; font-size: 13px;
                                 background: transparent; border: none; }}
            #donutLegendValue {{ color: #6B7280; font-size: 13px;
                                 background: transparent; border: none; }}
        """)
        if shadow:
            fx = QGraphicsDropShadowEffect(self)
            fx.setBlurRadius(24)
            fx.setOffset(0, 4)
            fx.setColor(QColor(27, 37, 89, 35))
            self.setGraphicsEffect(fx)

        self._show_percent = show_percent

        self._title = QLabel(title)
        self._title.setObjectName("donutCardTitle")

        self.chart = DonutChart(data, center_caption, center_value)

        self._legend_host = QWidget()
        self._legend_host.setStyleSheet("background: transparent;")
        self._legend = QGridLayout(self._legend_host)
        self._legend.setContentsMargins(0, 0, 0, 0)
        self._legend.setHorizontalSpacing(10)
        self._legend.setVerticalSpacing(8)

        self._body = QBoxLayout(QBoxLayout.LeftToRight)
        self._body.setSpacing(20)
        self._body.addWidget(self.chart, 1)
        self._body.addWidget(self._legend_host, 1, Qt.AlignVCenter)

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 16, 18, 16)
        root.setSpacing(10)
        root.addWidget(self._title)
        root.addLayout(self._body, 1)

        self.set_data(data)

    def set_title(self, title: str):
        self._title.setText(title)

    def set_center(self, caption: str = None, value=None):
        self.chart.set_center(caption, value)

    def set_data(self, data: Iterable[Item]):
        data = list(data)
        self.chart.set_data(data)
        self._rebuild_legend(data)

    def _set_stacked(self, stacked: bool):
        self._body.setDirection(
            QBoxLayout.TopToBottom if stacked else QBoxLayout.LeftToRight
        )
        self._body.setStretchFactor(self.chart, 1)
        self._body.setStretchFactor(self._legend_host, 0 if stacked else 1)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w = event.size().width()
        stacked = self._body.direction() == QBoxLayout.TopToBottom
        if not stacked and w < self.STACK_BELOW:
            self._set_stacked(True)
        elif stacked and w > self.STACK_BELOW + 40:
            self._set_stacked(False)

    def _rebuild_legend(self, data):
        while self._legend.count():
            w = self._legend.takeAt(0).widget()
            if w:
                w.deleteLater()

        total = sum(v for _, v, _ in data) or 1
        for row, (label, value, color) in enumerate(data):
            name = QLabel(label)
            name.setObjectName("donutLegendLabel")
            val_text = f"{value:g}"
            if self._show_percent:
                val_text += f" ({round(value / total * 100)}%)"
            val = QLabel(val_text)
            val.setObjectName("donutLegendValue")

            self._legend.addWidget(_LegendDot(color), row, 0, Qt.AlignVCenter)
            self._legend.addWidget(name, row, 1)
            self._legend.addWidget(val, row, 2, Qt.AlignRight)
        self._legend.setColumnStretch(1, 1)
