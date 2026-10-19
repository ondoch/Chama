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
    QFrame,
    QSizePolicy,
    QToolTip,
)

__all__ = ["LineChart", "GrowthCard"]


class LineChart(QWidget):
    MIN_LABEL_PX = 46
    HOVER_RADIUS = 16

    def __init__(self, labels=None, values=None, line_color="#2f5bff",
                 grid_color="#e6ebf5", text_color="#6b7280", y_max=None,
                 y_step=None, show_vgrid=True, fill=True,
                 tooltip_format="{label}: {value:g}", parent=None):
        super().__init__(parent)
        self.line_color = QColor(line_color)
        self.grid_color = QColor(grid_color)
        self.text_color = QColor(text_color)
        self.show_vgrid = show_vgrid
        self.fill = fill
        self._fixed_y_max = y_max
        self._fixed_y_step = y_step
        self.tooltip_format = tooltip_format
        self._hover = -1
        self.setMouseTracking(True)
        self.labels, self.values = [], []
        self.setMinimumSize(160, 110)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        if labels is not None and values is not None:
            self.set_data(labels, values)

    def set_data(self, labels, values):
        if len(labels) != len(values):
            raise ValueError("labels and values must be the same length")
        self.labels = list(labels)
        self.values = list(values)
        self._hover = -1
        self.update()

    def _axis(self):
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

    def _geometry(self):
        y_max, y_step = self._axis()
        left, right, top, bottom = 38, 10, 10, 26
        plot = QRectF(left, top, self.width() - left - right,
                      self.height() - top - bottom)
        step = plot.width() / len(self.values)
        pts = [QPointF(plot.left() + step * (i + 0.5),
                       plot.bottom() - (val / y_max) * plot.height())
               for i, val in enumerate(self.values)]
        return plot, pts, step, y_max, y_step, left

    def _point_at(self, pos):
        if not self.values:
            return -1
        _, pts, *_ = self._geometry()
        best, best_d = -1, self.HOVER_RADIUS
        for i, pt in enumerate(pts):
            d = math.hypot(pt.x() - pos.x(), pt.y() - pos.y())
            if d <= best_d:
                best, best_d = i, d
        return best

    def mouseMoveEvent(self, event):
        idx = self._point_at(event.pos())
        if idx != self._hover:
            self._hover = idx
            self.update()
            self.setCursor(Qt.PointingHandCursor if idx >= 0 else Qt.ArrowCursor)
        if idx >= 0:
            QToolTip.showText(
                event.globalPos(),
                self.tooltip_format.format(label=self.labels[idx], value=self.values[idx]),
                self,
            )
        else:
            QToolTip.hideText()

    def leaveEvent(self, event):
        if self._hover != -1:
            self._hover = -1
            self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        if not self.values:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        plot, pts, step, y_max, y_step, left = self._geometry()

        font = QFont()
        font.setPointSize(8)
        p.setFont(font)

        v = 0
        while v <= y_max + 1e-9:
            y = plot.bottom() - (v / y_max) * plot.height()
            p.setPen(QPen(self.grid_color, 1))
            p.drawLine(QPointF(plot.left(), y), QPointF(plot.right(), y))
            p.setPen(self.text_color)
            p.drawText(QRectF(0, y - 8, left - 6, 16),
                       Qt.AlignRight | Qt.AlignVCenter, f"{v:g}")
            v += y_step

        every = max(1, math.ceil(self.MIN_LABEL_PX / step)) if step > 0 else 1

        for i, pt in enumerate(pts):
            if self.show_vgrid:
                p.setPen(QPen(self.grid_color, 1))
                p.drawLine(QPointF(pt.x(), plot.top()),
                           QPointF(pt.x(), plot.bottom()))
            if i % every == 0:
                p.setPen(self.text_color)
                p.drawText(QRectF(pt.x() - 25, plot.bottom() + 6, 50, 16),
                           Qt.AlignCenter, str(self.labels[i]))

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

        path = QPainterPath(pts[0])
        for pt in pts[1:]:
            path.lineTo(pt)
        pen = QPen(self.line_color, 2.5)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setCapStyle(Qt.RoundCap)
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)
        p.drawPath(path)

        p.setPen(Qt.NoPen)
        p.setBrush(self.line_color)
        for pt in pts:
            p.drawEllipse(pt, 3.5, 3.5)

        if 0 <= self._hover < len(pts):
            p.setPen(QPen(QColor("white"), 2))
            p.setBrush(self.line_color)
            p.drawEllipse(pts[self._hover], 6, 6)


class GrowthCard(QFrame):

    def __init__(self, title="Growth", labels=None, values=None,
                 badge_text=None, line_color="#2f5bff",
                 tooltip_format="{label}: {value:g}", parent=None):
        super().__init__(parent)
        self.setObjectName("growthCard")
        self._title = QLabel(title)
        self._title.setObjectName("growthTitle")
        self._badge = QLabel()
        self._badge.setObjectName("growthBadge")
        self.chart = LineChart(line_color=line_color, tooltip_format=tooltip_format)

        header_container = QWidget()
        header = QHBoxLayout(header_container)
        header.setContentsMargins(0, 0, 0, 0)
        header.addWidget(self._title)
        header.addStretch()
        header.addWidget(self._badge)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 14)
        layout.setSpacing(10)
        layout.addWidget(header_container, alignment=Qt.AlignTop)
        layout.addWidget(self.chart, 1)

        self._apply_badge_style(positive=True)
        self._badge.hide()
        if labels is not None and values is not None:
            self.set_data(labels, values, badge_text)

    def set_title(self, text):
        self._title.setText(text)

    def set_data(self, labels, values, badge_text=None):
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
                color: #0f1b4c; font-size: 16px; font-weight: 600;
                background: transparent; border: none;
            }}
            #growthBadge {{
                background: {bg}; color: {fg};
                border-radius: 11px; padding: 3px 10px;
                font-size: 11px; font-weight: bold; border: none;
            }}
        """)
