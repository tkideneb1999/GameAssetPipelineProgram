from pathlib import Path
import re

from qtpy import QtWidgets as qtw
from qtpy import QtCore as qtc

from ..Common import spellcheckHelper as scH
from .tagDatabase_GUI import Ui_tagDatabase
from ..Common.Core.tagDatabase import TagDatabase


class TagDatabaseWidget(qtw.QWidget):
    s_tag_added = qtc.Signal(int, str)  # tag ID, tag name

    def __init__(self, parent=None):
        super(TagDatabaseWidget, self).__init__(parent)
        self.ui = Ui_tagDatabase()
        self.ui.setupUi(self)

        self.ui.add_tag_button.clicked.connect(self.add_tag)

        # Data
        self.project_dir: Path = None
        self.tag_database = TagDatabase()
        print("Tag Database:")
        print(self.tag_database)
        self.special_characters = re.compile(r'[@!#$%^&*()<>?/\|}{~:]')

    def load_tags(self, path: Path):
        self.project_dir = path
        self.tag_database.load(self.project_dir)
        self.update_view()

    def add_tag(self):
        text, ok = qtw.QInputDialog().getText(self, "Add Tag", "Tag Name:", qtw.QLineEdit.Normal, "")
        if not ok:
            return
        if text == "" or scH.contains_special_characters(text):
            print("[GAPA] Tag contains forbidden characters")
            self.add_tag()
        tid = self.tag_database.add_tag(text)
        if self.project_dir is not None:
            self.tag_database.save(self.project_dir)
        else:
            print("[GAPA] Can not save tags as there is no project dir")
        self.update_view()
        self.s_tag_added.emit(tid, text)

    def update_view(self):
        self.ui.tag_list.clear()
        for tag in self.tag_database.tag_names:
            self.ui.tag_list.addItem(tag)


