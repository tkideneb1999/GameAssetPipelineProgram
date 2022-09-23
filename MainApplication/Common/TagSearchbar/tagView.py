from qtpy import QtWidgets as qtw
from qtpy import QtCore as qtc
from qtpy import QtGui as qtg

from . import tagSearchbarConstants as tSC


class TagView(qtw.QWidget):

    s_deleted = qtc.Signal(str)
    s_selected = qtc.Signal(str)

    def __init__(self, tag_name: str, removable=True, parent=None):
        super().__init__(parent=parent)
        self.__removable = removable
        self.__name = tag_name
        self.font = qtg.QFont("Segoe UI", 9)
        fm = qtg.QFontMetrics(self.font)
        font_width = fm.horizontalAdvance(tag_name)
        self.init_height = tSC.TAG_HEIGHT
        # Width:
        # font width
        # X: 1 * Height
        # Ending Triangle: 0.5 * height
        # Circle: 0.5 * height
        # Text Padding : 2* tSC.TAG_TEXT_PADDING
        if removable:
            self.init_width = font_width + 2 * self.init_height + 2 * tSC.TAG_TEXT_PADDING
        else:
            self.init_width = font_width + 1 * self.init_height + 2 * tSC.TAG_TEXT_PADDING
        self.setMinimumSize(self.init_width, self.init_height)
        self.setMouseTracking(True)
        self.setSizePolicy(
            qtw.QSizePolicy.Fixed,
            qtw.QSizePolicy.Fixed
        )
        self.setFixedSize(self.init_width, self.init_height)

    def paintEvent(self, event):
        painter = qtg.QPainter(self)
        painter.setRenderHint(qtg.QPainter.RenderHint.Antialiasing, True)
        height = self.init_height
        width = self.init_width
        painter.setBrush(tSC.TAG_BACKGROUND_COLOR)
        painter.setPen(qtc.Qt.NoPen)

        # Tag Shape
        painter.begin(self)
        tri_start_x = int(width - height * 0.5)
        polygon = qtg.QPolygon()
        polygon << qtc.QPoint(0, 0)
        polygon << qtc.QPoint(tri_start_x, 0)
        polygon << qtc.QPoint(width, int(height * 0.5))
        polygon << qtc.QPoint(tri_start_x, height)
        polygon << qtc.QPoint(0, height)
        painter.drawConvexPolygon(polygon)

        # Circle
        center = qtc.QPoint(tri_start_x, int(height * 0.5))
        radius = height * 0.5 * tSC.TAG_CIRCLE_PADDING_PERCENT
        painter.setBrush(tSC.TAG_SEARCHBAR_BACKGROUND_COLOR)
        painter.drawEllipse(center, radius, radius)

        # Text
        painter.setPen(qtc.Qt.SolidLine)
        painter.setBrush(tSC.TAG_FONT_COLOR)
        if self.__removable:
            text_rect_start_pos = height + tSC.TAG_TEXT_PADDING
        else:
            text_rect_start_pos = tSC.TAG_TEXT_PADDING
        text_rect = qtc.QRect(
            text_rect_start_pos,
            tSC.TAG_TEXT_PADDING,
            width - height * 0.5 - radius - 2 * tSC.TAG_TEXT_PADDING,
            height - 2 * tSC.TAG_TEXT_PADDING
        )
        painter.setFont(self.font)
        painter.drawText(text_rect, qtc.Qt.AlignVCenter, self.__name)

        # X
        if self.__removable:
            lines = [
                qtc.QLine(
                    height * tSC.TAG_REMOVE_PADDING_PERCENT,
                    height * tSC.TAG_REMOVE_PADDING_PERCENT,
                    height * (1 - tSC.TAG_REMOVE_PADDING_PERCENT),
                    height * (1 - tSC.TAG_REMOVE_PADDING_PERCENT)
                ),
                qtc.QLine(
                    height * tSC.TAG_REMOVE_PADDING_PERCENT,
                    height * (1 - tSC.TAG_REMOVE_PADDING_PERCENT),
                    height * (1 - tSC.TAG_REMOVE_PADDING_PERCENT),
                    height * tSC.TAG_REMOVE_PADDING_PERCENT
                ),
            ]
            pen = painter.pen()
            pen.setWidth(2)
            pen.setColor(tSC.TAG_X_COLOR)
            painter.setPen(pen)
            painter.drawLines(lines)

        painter.end()
        super().paintEvent(event)

    def mouseReleaseEvent(self, event: qtg.QMouseEvent) -> None:
        if not self.__removable:
            super().mouseReleaseEvent(event)
            return
        remove_rect = qtc.QRect(0, 0, self.init_height, self.init_height)
        if remove_rect.contains(event.pos()):
            print(f"Removing Tag: {self.__name}")
            self.s_deleted.emit(self.__name)
        elif self.rect().contains(event.pos()):
            print(f"Selected Tag: {self.__name}")
            self.s_selected.emit(self.__name)
        super().mouseReleaseEvent(event)