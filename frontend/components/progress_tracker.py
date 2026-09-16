import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QVBoxLayout, QPushButton,
                              QHBoxLayout, QSizePolicy)
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush, QFontMetrics
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QSize


class StepProgressTracker(QWidget):

    stepChanged = pyqtSignal(int)

    def __init__(self, steps, current_step=0, parent=None):
        super().__init__(parent)
        self._steps = list(steps)
        self._current = current_step

        self.circle_radius = 14
        self.circle_gap_top = 18
        self.label_gap = 10
        self.line_width = 2

        self.min_step_width = 130
        self.side_margin = 20

        self.color_active = QColor("#1b2a6b")
        self.color_inactive_border = QColor("#1b2a6b")
        self.color_inactive_fill = QColor("#ffffff")
        self.color_line_done = QColor("#1b2a6b")
        self.color_line_todo = QColor("#c7ccd9")
        self.color_label_active = QColor("#1b2a6b")
        self.color_label_inactive = QColor("#8a7a3a")

        self.setMinimumHeight(80)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)

    def _layout_metrics(self):
        n = max(len(self._steps), 1)
        label_font = QFont(self.font())
        label_font.setPointSize(9)
        label_font.setBold(True)
        fm = QFontMetrics(label_font)
        widest_label = max((fm.horizontalAdvance(s) for s in self._steps), default=0)
        step_width = max(self.min_step_width, widest_label + 20)
        margin = step_width / 2
        return n, step_width, margin

    def sizeHint(self):
        n, step_width, margin = self._layout_metrics()
        width = step_width * (n - 1) + 2 * margin
        return QSize(int(width), self.minimumHeight())

    def set_steps(self, steps):
        self._steps = list(steps)
        self.updateGeometry()
        self.update()

    def set_current_step(self, index):
        index = max(0, min(index, len(self._steps) - 1))
        if index != self._current:
            self._current = index
            self.stepChanged.emit(index)
            self.update()

    @property
    def current_step(self):
        return self._current

    def next_step(self):
        self.set_current_step(self._current + 1)

    def previous_step(self):
        self.set_current_step(self._current - 1)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        n = len(self._steps)
        if n == 0:
            return

        r = self.circle_radius
        cy = self.circle_gap_top + r

        _, step_width, margin = self._layout_metrics()
        content_width = step_width * (n - 1) + 2 * margin
        x_offset = max(0.0, (self.width() - content_width) / 2)
        step_gap = step_width
        centers_x = [x_offset + margin + i * step_gap for i in range(n)]

        pen = QPen()
        pen.setWidth(self.line_width)
        for i in range(n - 1):
            x1 = centers_x[i] + r
            x2 = centers_x[i + 1] - r
            done = i < self._current
            pen.setColor(self.color_line_done if done else self.color_line_todo)
            painter.setPen(pen)
            painter.drawLine(int(x1), int(cy), int(x2), int(cy))

        num_font = QFont(self.font())
        num_font.setBold(True)
        num_font.setPointSize(10)
        painter.setFont(num_font)

        for i, x in enumerate(centers_x):
            rect = QRectF(x - r, cy - r, 2 * r, 2 * r)
            if i <= self._current:
                painter.setBrush(QBrush(self.color_active))
                painter.setPen(QPen(self.color_active, 1))
                text_color = QColor("#ffffff")
            else:
                painter.setBrush(QBrush(self.color_inactive_fill))
                painter.setPen(QPen(self.color_inactive_border, 1.5))
                text_color = self.color_inactive_border
            painter.drawEllipse(rect)

            painter.setPen(QPen(text_color))
            painter.drawText(rect, Qt.AlignCenter, str(i + 1))

        label_font = QFont(self.font())
        label_font.setPointSize(9)
        label_y_top = cy + r + self.label_gap
        label_h = self.minimumHeight() - label_y_top - 4

        for i, x in enumerate(centers_x):
            label_font.setBold(i == self._current)
            painter.setFont(label_font)
            painter.setPen(QPen(self.color_label_active if i == self._current
                                 else self.color_label_inactive))
            half_w = margin - 4
            label_rect = QRectF(x - half_w, label_y_top, 2 * half_w, label_h)
            painter.drawText(label_rect, Qt.AlignHCenter | Qt.AlignTop | Qt.TextWordWrap,
                              self._steps[i])

        painter.end()
