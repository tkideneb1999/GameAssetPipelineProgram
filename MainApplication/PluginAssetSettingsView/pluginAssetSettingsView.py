from PyQt5 import QtWidgets as qtw
import functools


class PluginAssetSettingsView(qtw.QDialog):
    def __init__(self, settings: dict, enable_execute=False, saved_settings=None, outputs=None, parent=None):
        super(PluginAssetSettingsView, self).__init__(parent)

        # GUI Types
        self.gui_types = {"lineedit": self.add_lineedit,
                          "combobox": self.add_combobox,
                          "checkbox": self.add_checkbox}
        self.execute_clicked = False
        self.gui_elements = {}

        self.settings = {}
        self.current_output = None
        self.dialog_layout = qtw.QVBoxLayout(self)
        self.setLayout(self.dialog_layout)

        self.tab_widget = qtw.QTabWidget(self)
        self.tab_widget.setTabPosition(qtw.QTabWidget.West)
        self.tabs: dict[str, qtw.QWidget] = {}
        self.create_tab("General")
        self.dialog_layout.addWidget(self.tab_widget)

        for name in settings:
            gui_type = settings[name]["type"]
            func = self.gui_types.get(gui_type)
            if func is None:
                print(f"[GAPA] Function type is either not spelled correctly or does not exist")
                continue
            self.gui_types[gui_type](name, settings[name]["data"], settings[name]["tab"])

        if saved_settings is not None:
            self.set_all_settings(saved_settings)

        self.outputs = outputs
        if outputs is not None:
            self.output_list = qtw.QListWidget(self)
            output_strings = [f"{o[0]}, {o[1]}" for o in self.outputs]
            self.output_list.addItems(output_strings)
            self.output_list.currentRowChanged.connect(self.selected_output)

        self.button_layout = qtw.QHBoxLayout(self)

        self.save_button = qtw.QPushButton("Save", self)
        self.save_button.clicked.connect(self.accept)
        self.button_layout.addWidget(self.save_button)

        self.cancel_button = qtw.QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)
        self.button_layout.addWidget(self.cancel_button)

        if enable_execute:
            self.execute_button = qtw.QPushButton("Execute", self)
            self.execute_button.clicked.connect(self.click_execute)
            self.button_layout.addWidget(self.execute_button)

        self.dialog_layout.addLayout(self.button_layout)

    def create_tab(self, name: str) -> None:
        self.tabs[name] = qtw.QWidget(self.tab_widget)
        layout = qtw.QVBoxLayout(self.tabs[name])
        self.tabs[name].setLayout(layout)
        self.tab_widget.addTab(self.tabs[name], name)
        print(f"[GAPA] created Tab: {name}")

    def add_lineedit(self, name: str, default_value, tab: str) -> None:
        lineedit = qtw.QLineEdit(self)
        lineedit.setObjectName(name)
        if default_value is not None:
            lineedit.setText(default_value)
            self.settings[name] = default_value
        else:
            self.settings[name] = ""
        text_changed = functools.partial(self.set_setting, name=name)
        lineedit.textChanged.connect(text_changed)

        label = qtw.QLabel(self)
        label.setText(name)

        layout = qtw.QHBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(lineedit)

        self.gui_elements[name] = [lineedit, label, layout]

        self.add_layout_to_tab(layout, tab)

    def add_combobox(self, name: str, data, tab: str) -> None:
        combobox = qtw.QComboBox(self)
        combobox.setObjectName(name)
        combobox.addItems(data)

        self.settings[name] = data[0]

        def selected(selected_entry):
            self.set_setting(name, selected_entry)
        selection_changed = functools.partial(selected)
        combobox.currentTextChanged.connect(selection_changed)

        label = qtw.QLabel(self)
        label.setText(name)

        layout = qtw.QHBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(combobox)

        self.gui_elements[name] = [combobox, label, layout]
        # self.dialog_layout.addLayout(layout)
        self.add_layout_to_tab(layout, tab)

    def add_checkbox(self, name: str, default_value: bool, tab: str) -> None:
        checkbox = qtw.QCheckBox(self)
        checkbox.setObjectName(name)
        checkbox.setText(name)
        checkbox.setChecked(default_value)

        self.settings[name] = default_value

        checked_changed = functools.partial(self.set_setting, name=name)
        checkbox.toggled.connect(checked_changed)

        self.gui_elements[name] = [checkbox]

        self.add_widget_to_tab(checkbox, tab)

    def add_widget_to_tab(self, widget: qtw.QWidget, tab_name):
        tab_widget = self.tabs.get(tab_name)
        if tab_widget is None:
            self.create_tab(tab_name)
            tab_widget = self.tabs.get(tab_name)
        tab_widget.layout().addWidget(widget)

    def add_layout_to_tab(self, layout: qtw.QLayout, tab_name):
        tab_widget = self.tabs.get(tab_name)
        if tab_widget is None:
            self.create_tab(tab_name)
            tab_widget = self.tabs.get(tab_name)
        tab_widget.layout().addLayout(layout)

    def get_settings(self) -> dict:
        return self.settings

    def set_setting(self, name: str, value) -> None:
        self.settings[name] = value

    def click_execute(self):
        self.execute_clicked = True
        self.accept()

    def set_all_settings(self, settings: dict) -> None:
        for gui_name in self.gui_elements:
            data = settings.get(gui_name)
            if data is None:
                print(f"No data found for setting: {gui_name}")
                continue
            gui_type = type(self.gui_elements[gui_name][0])
            if gui_type == qtw.QCheckBox:
                self.gui_elements[gui_name][0].setChecked(data)
            elif gui_type == qtw.QLineEdit:
                self.gui_elements[gui_name][0].setText(data)
            elif gui_type == qtw.QComboBox:
                self.gui_elements[gui_name][0].setCurrentText(data)

    def selected_output(self, index: int):
        self.current_output = self.outputs[index]

