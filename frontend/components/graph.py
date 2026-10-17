import math

from PyQt5.QtCore import (
    Qt,
    QRectF,
    QPointF
)
from PyQt5.QtGui import (
    QPainter,
    QColor,
    QPen,
    QBrush,
    QLinearGradient,
    QPainterPath,
    QFont
)
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame
)

__all__ = ["LineChart", "GrowthCard"]


class LineChart(QWidget):

    def __init__(self, labels=None, values=None, line_color="#2f5bff",
                 grid_color="#e6ebf5", text_color="#6b7280", y_max=None,
                 y_step=None, show_vgrid=True, fill=True, parent=None):
        super().__init__(parent)
        self.line_color = QColor(line_color)
        self.grid_color = QColor(grid_color)
        self.text_color = QColor(text_color)
        self.show_vgrid = show_vgrid
        self.fill = fill
        self._fixed_y_max = y_max
        self._fixed_y_step = y_step
        self.labels, self.values = [], []
        self.setMinimumSize(300, 180)
        if labels is not None and values is not None:
            self.set_data(labels, values)

    def set_data(self, labels, values):
        if len(labels) != len(values):
            raise ValueError("labels and values must be the same length")
        self.labels = list(labels)
        self.values = list(values)
        self.update()

    def _axis(self):
        """Return (y_max, y_step), auto-picked when not fixed."""
        if self._fixed_y_max is not None:
            y_max = self._fixed_y_max
            step = self._fixed_y_step or y_max / 5
            return y_max, step
        peak = max(self.values) if self.values else 1
        step = self._fixed_y_step or self._nice_step(peak / 5)
        y_max = math.ceil(peak / step) * step or step
        return y_max, step

    @staticmethod
    def _nice_step(raw):
        if raw <= 0:
            return 1
        mag = 10 ** math.floor(math.log10(raw))
        for m in (1, 2, 5, 10):
            if raw <= m * mag:
                return m * mag
        return 10 * mag

    # ---------- painting ----------
    def paintEvent(self, event):
        if not self.values:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        y_max, y_step = self._axis()
        left, right, top, bottom = 38, 10, 10, 26
        plot = QRectF(left, top, self.width() - left - right,
                      self.height() - top - bottom)

        font = QFont()
        font.setPointSize(8)
        p.setFont(font)

        # horizontal grid + y labels
        v = 0
        while v <= y_max + 1e-9:
            y = plot.bottom() - (v / y_max) * plot.height()
            p.setPen(QPen(self.grid_color, 1))
            p.drawLine(QPointF(plot.left(), y), QPointF(plot.right(), y))
            p.setPen(self.text_color)
            p.drawText(QRectF(0, y - 8, left - 6, 16),
                       Qt.AlignRight | Qt.AlignVCenter, f"{v:g}")
            v += y_step

        # points
        n = len(self.values)
        step = plot.width() / n
        pts = [QPointF(plot.left() + step * (i + 0.5),
                       plot.bottom() - (val / y_max) * plot.height())
               for i, val in enumerate(self.values)]

        # vertical grid + x labels
        for i, pt in enumerate(pts):
            if self.show_vgrid:
                p.setPen(QPen(self.grid_color, 1))
                p.drawLine(QPointF(pt.x(), plot.top()),
                           QPointF(pt.x(), plot.bottom()))
            p.setPen(self.text_color)
            p.drawText(QRectF(pt.x() - 25, plot.bottom() + 6, 50, 16),
                       Qt.AlignCenter, str(self.labels[i]))

        # gradient fill
        if self.fill:
            area = QPainterPath()
            area.moveTo(pts[0].x(), plot.bottom())
            for pt in pts:
                area.lineTo(pt)
            area.lineTo(pts[-1].x(), plot.bottom())
            area.closeSubpath()
            grad = QLinearGradient(0, plot.top(), 0, plot.bottom())
            c1, c2 = QColor(self.line_color), QColor(self.line_color)
            c1.setAlpha(70)
            c2.setAlpha(5)
            grad.setColorAt(0, c1)
            grad.setColorAt(1, c2)
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(grad))
            p.drawPath(area)

        # line
        path = QPainterPath(pts[0])
        for pt in pts[1:]:
            path.lineTo(pt)
        pen = QPen(self.line_color, 2.5)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setCapStyle(Qt.RoundCap)
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)
        p.drawPath(path)

        # dots
        p.setPen(Qt.NoPen)
        p.setBrush(self.line_color)
        for pt in pts:
            p.drawEllipse(pt, 3.5, 3.5)


class GrowthCard(QFrame):

    def __init__(self, title="Growth", labels=None, values=None,
                 badge_text=None, line_color="#2f5bff", parent=None):
        super().__init__(parent)
        self.setObjectName("growthCard")
        self._title = QLabel(title)
        self._title.setObjectName("growthTitle")
        self._badge = QLabel()
        self._badge.setObjectName("growthBadge")
        self.chart = LineChart(line_color=line_color)

        header_container = QWidget()
        header = QHBoxLayout(header_container)
        header.addWidget(self._title)
        header.addStretch()
        header.addWidget(self._badge)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 14)
        layout.setSpacing(10)
        layout.addWidget(header_container, alignment=Qt.AlignTop)
        layout.addWidget(self.chart)

        self._apply_badge_style(positive=True)
        self._badge.hide()
        if labels is not None and values is not None:
            self.set_data(labels, values, badge_text)

    # ---------- public API ----------
    def set_title(self, text):
        self._title.setText(text)

    def set_data(self, labels, values, badge_text=None):
        """Update the chart. If badge_text is None, shows % change first->last."""
        self.chart.set_data(labels, values)
        if badge_text is None:
            badge_text = self._auto_badge(values)
        self.set_badge(badge_text, positive=not badge_text.startswith("\u2198"))

    def set_badge(self, text, positive=True):
        if not text:
            self._badge.hide()
            return
        self._badge.setText(text)
        self._apply_badge_style(positive)
        self._badge.show()

    # ---------- internals ----------
    @staticmethod
    def _auto_badge(values):
        if len(values) < 2 or values[0] == 0:
            return ""
        pct = (values[-1] - values[0]) / abs(values[0]) * 100
        arrow = "\u2197" if pct >= 0 else "\u2198"
        return f"{arrow} {abs(pct):.0f}%"

    def _apply_badge_style(self, positive):
        bg, fg = ("#dcfce7", "#16a34a") if positive else ("#fee2e2", "#dc2626")
        self.setStyleSheet(f"""
            #growthCard {{
                background: white;
                border: 1px solid #e5e9f2;
                border-radius: 16px;
            }}
            #growthTitle {{
                color: #0f1b4c; font-size: 15px; font-weight: bold;
            }}
            #growthBadge {{
                background: {bg}; color: {fg};
                border-radius: 11px; padding: 3px 10px;
                font-size: 11px; font-weight: bold;
            }}
        """)
