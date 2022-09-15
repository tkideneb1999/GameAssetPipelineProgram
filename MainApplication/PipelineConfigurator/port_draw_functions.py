from qtpy import QtCore as qtc
from qtpy import QtGui as qtg


def draw_square_port(painter, rect, info):
    painter.save()

    # mouse over port color.
    if info['hovered']:
        color = qtg.QColor(14, 45, 59)
        border_color = qtg.QColor(136, 255, 35, 255)
    # port connected color.
    elif info['connected']:
        color = qtg.QColor(195, 60, 60)
        border_color = qtg.QColor(200, 130, 70)
    # default port color
    else:
        color = qtg.QColor(*info['color'])
        border_color = qtg.QColor(*info['border_color'])

    pen = qtg.QPen(border_color, 1.8)
    pen.setJoinStyle(qtc.Qt.MiterJoin)

    painter.setPen(pen)
    painter.setBrush(color)
    painter.drawRect(rect)

    painter.restore()


def draw_triangle_port(painter, rect, info):
    painter.save()

    size = int(rect.height() / 2)
    triangle = qtg.QPolygonF()
    triangle.append(qtc.QPointF(-size, size))
    triangle.append(qtc.QPointF(0.0, -size))
    triangle.append(qtc.QPointF(size, size))

    transform = qtg.QTransform()
    transform.translate(rect.center().x(), rect.center().y())
    port_poly = transform.map(triangle)

    # mouse over port color.
    if info['hovered']:
        color = qtg.QColor(14, 45, 59)
        border_color = qtg.QColor(136, 255, 35)
    # port connected color.
    elif info['connected']:
        color = qtg.QColor(195, 60, 60)
        border_color = qtg.QColor(200, 130, 70)
    # default port color
    else:
        color = qtg.QColor(*info['color'])
        border_color = qtg.QColor(*info['border_color'])

    pen = qtg.QPen(border_color, 1.8)
    pen.setJoinStyle(qtc.Qt.MiterJoin)

    painter.setPen(pen)
    painter.setBrush(color)
    painter.drawPolygon(port_poly)

    painter.restore()


PORT_DATA_TYPE_MAP = {
    "texture": draw_square_port,
    "tga": draw_square_port,
    "tiff": draw_square_port,
    "png": draw_square_port,
    "jpg": draw_square_port,
    "mesh": draw_triangle_port,
    "fbx": draw_triangle_port,
    "obj": draw_triangle_port,
}