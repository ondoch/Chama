FONT_FAMILY = "Segoe UI"

COLOR_TEXT_PRIMARY = "#1F2937"
COLOR_TEXT_MUTED = "#869DA7"
COLOR_ACCENT_BLUE = "#0062D1"
COLOR_ACCENT_BLUE_BG = "#B8D4FF"
COLOR_ACCENT_GREEN = "#14BD55"
COLOR_ACCENT_GREEN_BG = "#BEF8D5"
COLOR_ACCENT_GREEN_BORDER = "#18E767"
COLOR_ACCENT_RED_BG = "#FFE6E6"
COLOR_ACCENT_RED_BORDER = "#A30000"
COLOR_CARD_BG = "#FFFFFF"
COLOR_PANEL_BG = "#E6F1FF"
COLOR_BORDER = "#D8DBDE"
COLOR_SIDEBAR_BG = "#004CA3"
COLOR_SIDEBAR_HOVER = "#0062D1"
COLOR_SIDEBAR_SELECT = "#2E8FFF"


def label_style(size=13, weight=400, color=COLOR_TEXT_MUTED, transparent=False):
    bg = "background: transparent;" if transparent else ""
    return f"""
        font-family: '{FONT_FAMILY}';
        font-size: {size}px;
        font-weight: {weight};
        color: {color};
        {bg}
    """


def add_shadow(widget, blur=0.5, x_offset=1, y_offset=1, color=(31, 41, 55, 35)):
    from PyQt5.QtWidgets import QGraphicsDropShadowEffect
    from PyQt5.QtGui import QColor
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(blur)
    shadow.setXOffset(x_offset)
    shadow.setYOffset(y_offset)
    shadow.setColor(QColor(*color))
    widget.setGraphicsEffect(shadow)