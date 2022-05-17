from pathlib import Path
import re

from PyQt5 import QtWidgets as qtw

from .. import spellcheckHelper as scH
from .tagDatabase_GUI import Ui_tagDatabase
from.tagDatabase import TagDatabase


class TagDatabaseWidget(qtw.QWidget):
    def __init__(self, parent=None):
        super(TagDatabaseWidget, self).__init__(parent)
        self.ui = Ui_tagDatabase()
        self.ui.setupUi(self)

        self.ui.add_tag_button.clicked.connect(self.add_tag)

        # Data
        self.project_dir: Path = None
        self.tag_database = TagDatabase()
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
        self.tag_database.add_tag(text)
        if self.project_dir is not None:
            self.tag_database.save(self.project_dir)
        else:
            print("[GAPA] Can not save tags as there is no project dir")
        self.update_view()

    def update_view(self):
        self.ui.tag_list.clear()
        for uid in self.tag_database.tags:
            self.ui.tag_list.addItem(self.tag_database.tags[uid])

