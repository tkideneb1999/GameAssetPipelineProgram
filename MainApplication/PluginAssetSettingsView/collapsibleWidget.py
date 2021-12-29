from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


def clickable(widget: qtw.QWidget):
    class Filter(qtc.QObject):

        s_clicked = qtc.pyqtSignal()

        def eventFilter(self, source: qtc.QObject, event: qtc.QEvent) -> bool:
            if source == widget:
                clicked = False
                if event.type() == qtc.QEvent.MouseButtonRelease:
                    if event.button() == qtc.Qt.LeftButton:
                        if source.rect().contains(event.pos()):
                            self.s_clicked.emit()
                            clicked = True
                return clicked or super().eventFilter(source, event)

            return super().eventFilter(source, event)

    event_filter = Filter(widget)
    widget.installEventFilter(event_filter)
    return event_filter.s_clicked


class CollapsibleWidget(qtw.QWidget):
    def __init__(self, label="Collapsible", parent=None):
        super(CollapsibleWidget, self).__init__(parent)
        size_policy = qtw.QSizePolicy(qtw.QSizePolicy.MinimumExpanding, qtw.QSizePolicy.MinimumExpanding)
        self.setSizePolicy(size_policy)
        self.complete_layout = qtw.QVBoxLayout()
        self.complete_layout.setContentsMargins(9, 9, 9, 9)
        self.complete_layout.setAlignment(qtc.Qt.AlignTop)

        self.header = qtw.QLabel(label)
        self.header.setFrameShape(qtw.QFrame.Box)
        font = qtg.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.header.setFont(font)
        header_size_policy = qtw.QSizePolicy(qtw.QSizePolicy.MinimumExpanding, qtw.QSizePolicy.Fixed)
        self.header.setMinimumHeight(15)
        self.header.setSizePolicy(header_size_policy)

        clicked_signal = clickable(self.header)
        clicked_signal.connect(self.toggle_collapse_widget)

        self.complete_layout.addWidget(self.header)

        self.widgets_frame = qtw.QFrame(parent=self)
        self.widgets_frame.setFrameShape(qtw.QFrame.StyledPanel)
        self.widgets_frame.setLineWidth(10)
        self.widgets_frame.setSizePolicy(size_policy)

        self.frame_layout = qtw.QVBoxLayout(self)
        self.frame_layout.setContentsMargins(30, 0, 0, 0)
        self.frame_layout.addWidget(self.widgets_frame)

        self.container_widget = qtw.QWidget(self)
        container_size_policy = self.container_widget.sizePolicy()
        container_size_policy.setRetainSizeWhenHidden(False)
        self.container_widget.setSizePolicy(container_size_policy)
        self.container_widget.setLayout(self.frame_layout)
        self.complete_layout.addWidget(self.container_widget)

        self.setLayout(self.complete_layout)
        self.widgets_layout = qtw.QVBoxLayout()
        self.widgets_frame.setLayout(self.widgets_layout)

        self.widgets_layout.addWidget(qtw.QLabel("Test"))

        self.is_collapsed = False

    def toggle_collapse_widget(self) -> None:
        if self.is_collapsed:
            self.container_widget.show()
            self.is_collapsed = False
        else:
            self.container_widget.hide()
            self.is_collapsed = True
