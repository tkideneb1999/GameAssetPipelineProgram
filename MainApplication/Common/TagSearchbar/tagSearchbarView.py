import difflib

from qtpy import QtWidgets as qtw
from qtpy import QtGui as qtg
from qtpy import QtCore as qtc

from . import tagSearchbarConstants as tSC
from .tagView import TagView


class TagSearchbarView(qtw.QWidget):

    s_added_tag = qtc.Signal(str)
    s_removed_tag = qtc.Signal(str)

    def __init__(self, tag_list=None, parent=None):
        super().__init__(parent=parent)

        # Data
        if tag_list is None:
            self.__tag_pool = []
        else:
            self.__tag_pool = tag_list
        self.__selected_tags = {}

        # UI Init
        # Colors
        self.background_color = tSC.TAG_SEARCHBAR_BACKGROUND_COLOR
        self.border_color = tSC.TAG_SEARCHBAR_BORDER_COLOR

        self.init_height = 25
        self.init_width = 200
        self.setMinimumSize(self.init_width, self.init_height)
        self.setSizePolicy(
            qtw.QSizePolicy.MinimumExpanding,
            qtw.QSizePolicy.Fixed
        )
        self.h_layout = qtw.QHBoxLayout(self)
        self.h_layout.setContentsMargins(5, 3, 5, 3)
        self.setLayout(self.h_layout)

        # Tag Edit
        self.tag_edit = qtw.QLineEdit(self)
        self.tag_edit.setFrame(False)
        self.tag_edit.textChanged.connect(self.textChanged)
        self.tag_edit.returnPressed.connect(self.returnPressed)
        self.h_layout.addWidget(self.tag_edit)
        if len(self.__tag_pool) == 0:
            self.tag_edit.setDisabled(True)

        # Tag Selector
        self.tag_selector = TagSelectorView(parent)
        self.tag_selector.s_tag_selected.connect(self.add_tag)
        self.tag_selector.hide()

        self.spacer = qtw.QSpacerItem(1, self.init_height - 2, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        self.h_layout.addSpacerItem(self.spacer)

    def paintEvent(self, event: qtg.QPaintEvent) -> None:
        painter = qtg.QPainter(self)
        painter.save()

        # UI Init
        pen = painter.pen()
        pen.setColor(self.border_color)
        painter.setPen(pen)
        brush = painter.brush()
        brush.setColor(self.background_color)
        painter.setBrush(brush)

        # Draw UI
        panel_rect = qtc.QRect(1, 1, self.width() - 1, self.height() - 1)
        painter.drawRect(panel_rect)

        painter.restore()
        super().paintEvent(event)

    def moveEvent(self, event: qtg.QMoveEvent) -> None:
        print("Move")
        new_pos = self.mapToGlobal(qtc.QPoint(self.tag_edit.pos().x(), self.height()))
        self.tag_selector.move(new_pos)
        super().moveEvent(event)

    def textChanged(self, text):
        # Update TagSelectorView
        if text == "":
            self.tag_selector.hide()
            return

        # global_pos = self.pos() + qtc.QPoint(self.tag_edit.pos().x(), self.height())
        global_pos = self.mapToGlobal(qtc.QPoint(self.tag_edit.pos().x(), self.height()))
        selectable_tags = self.calculate_tag_similarity(text, tSC.TAG_SELECTOR_MAX_TAGS)
        if len(selectable_tags) == 0:
            self.tag_selector.hide()
            return
        self.tag_selector.update_selector(selectable_tags, global_pos)
        self.tag_selector.show()

    def returnPressed(self) -> None:
        selected_tags = self.calculate_tag_similarity(self.tag_edit.text(), 1)
        if len(selected_tags) == 0:
            return
        self.add_tag(selected_tags[0])

    def calculate_tag_similarity(self, text, max_entries) -> list:  # TODO: Rework finding top 5 tags
        """
        Calculates similarity of the text with the tags present
        :param text: text to check tag similarity against
        :param max_entries: maximum number of entries to return
        :returns: List of tags ranked from biggest similarity at the start to smallest similarity at the end
        """
        # Calculate similarity ration
        similarities = {}  # index: similarity
        for i in range(len(self.__tag_pool)):
            similarities[i] = difflib.SequenceMatcher(None, text, self.__tag_pool[i]).ratio()
        # Order tags in new list based on highest similarity first
        similarity_ordered = []
        for i in range(max_entries):
            highest = (-1, 0.0)  # index, similarity
            for s in similarities:
                if similarities[s] > highest[1]:
                    highest = (s, similarities[s])
            if highest[0] == -1:
                break
            similarity_ordered.append(self.__tag_pool[highest[0]])
            similarities.pop(highest[0])
        return similarity_ordered

    def add_tag(self, tag: str) -> None:
        """
        Adds tag to selected tags
        :param tag: tag name
        """
        tag_widget = TagView(tag)
        tag_widget.s_deleted.connect(self.delete_tag)
        self.__tag_pool.remove(tag)
        self.__selected_tags[tag] = tag_widget
        index = self.h_layout.count() - 2
        self.h_layout.insertWidget(index, tag_widget)
        self.tag_edit.clear()

    def delete_tag(self, tag: str) -> None:
        """
        Removes tag from the selected ones
        :param tag: tag name
        """
        self.__tag_pool.append(tag)
        widget: TagView = self.__selected_tags.pop(tag)
        widget.deleteLater()

    def update_tags(self, new_tag_list: list) -> None:
        """
        Overwrites current present tag list with new one
        :param new_tag_list: new list of tags that replaces the old one
        """
        if len(new_tag_list) == 0:
            return
        self.tag_edit.setEnabled(True)
        # Check if selected tags are present in new tag list
        not_existing_tags = []
        for t in self.__selected_tags:
            if t not in new_tag_list:
                not_existing_tags.append(t)

        # remove selected tags if not present
        for t in not_existing_tags:
            self.delete_tag(t)

        # add non selected tags of new tag list to pool
        self.__tag_pool.clear()
        for nt in new_tag_list:
            if nt not in self.__selected_tags:
                self.__tag_pool.append(nt)

    @property
    def selected_tags(self):
        return list(self.__selected_tags.keys())


class TagSelectorView(qtw.QWidget):

    s_tag_selected = qtc.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Data
        self.tags: dict[TagView] = {}

        # UI Init
        # Colors
        self.background_color = tSC.TAG_SELECTOR_BACKGROUND_COLOR
        self.border_color = tSC.TAG_SELECTOR_BORDER_COLOR

        self.v_layout = qtw.QVBoxLayout(self)
        self.v_layout.setContentsMargins(3, 3, 3, 3)
        self.v_layout.setSpacing(3)
        self.setLayout(self.v_layout)
        self.setWindowFlag(qtc.Qt.WindowStaysOnTopHint)
        self.setWindowFlag(qtc.Qt.Window)
        self.setWindowFlag(qtc.Qt.FramelessWindowHint)

    def paintEvent(self, event: qtg.QPaintEvent) -> None:
        painter = qtg.QPainter(self)
        painter.save()

        # Painter Init
        pen = painter.pen()
        pen.setColor(self.border_color)
        painter.setPen(pen)
        brush = painter.brush()
        brush.setColor(self.background_color)
        painter.setBrush(brush)

        # Draw UI
        panel_rect = qtc.QRect(1, 1, self.width() - 1, self.height() - 1)
        painter.drawRect(panel_rect)

        painter.restore()
        super().paintEvent(event)

    def update_selector(self, tags: list, global_pos: qtc.QPoint):
        for w in self.tags.values():
            self.v_layout.removeWidget(w)
            w.deleteLater()
        self.tags.clear()
        selector_width = 0
        max_tags = min(len(tags), tSC.TAG_SELECTOR_MAX_TAGS)
        for i in range(max_tags):
            t = tags[i]
            self.tags[t] = TagView(t, False, self)
            self.v_layout.addWidget(self.tags[t])
            if self.tags[t].rect().width() > selector_width:
                selector_width = self.tags[t].rect().width()

        selector_width += self.v_layout.contentsMargins().left() + self.v_layout.contentsMargins().right()
        height_contents_margin = self.v_layout.contentsMargins().top() + self.v_layout.contentsMargins().bottom()
        selector_height = len(self.tags) * (self.v_layout.spacing() + tSC.TAG_HEIGHT) + height_contents_margin
        self.setFixedSize(selector_width, selector_height)
        self.move(global_pos)
        self.update()

    def mouseReleaseEvent(self, event: qtg.QMouseEvent) -> None:
        if self.rect().contains(event.pos()):
            for t in self.tags:
                w: TagView = self.tags[t]
                rect = qtc.QRect(w.pos().x(), w.pos().y(), w.width(), w.height())
                if rect.contains(event.pos()):
                    print(f"Tag selected: {t}")
                    self.s_tag_selected.emit(t)
                    break
        super().mouseReleaseEvent(event)

