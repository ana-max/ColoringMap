from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel,\
    QLineEdit, QPushButton
from PyQt5.QtGui import QIcon


class Saver(QWidget):
    def __init__(self, func_for_click):
        super().__init__()
        self.func_for_click = func_for_click
        self.create_gui()

    def create_gui(self):
        self.save = QLabel('Save To:')
        self.save_edit = QLineEdit()
        self.save_button = QPushButton('Save')

        grid = QGridLayout()
        grid.setSpacing(0)
        grid.addWidget(self.save, 0, 0)
        grid.addWidget(self.save_edit, 2, 0)
        grid.addWidget(self.save_button)
        self.save_button.clicked.connect(self.func_for_click)
        self.setLayout(grid)
        self.setGeometry(300, 300, 400, 100)
        self.setWindowTitle('Save as')
        self.setWindowIcon(QIcon(r'icons\icon_directory.png'))


class Loader(QWidget):
    def __init__(self, func_for_click):
        super().__init__()
        self.func_for_click = func_for_click
        self.create_gui()

    def create_gui(self):
        self.load = QLabel('Load from:')
        self.load_edit = QLineEdit()
        self.save_button = QPushButton('Load')

        grid = QGridLayout()
        grid.setSpacing(0)
        grid.addWidget(self.load, 0, 0)
        grid.addWidget(self.load_edit, 2, 0)
        grid.addWidget(self.save_button)
        self.save_button.clicked.connect(self.func_for_click)
        self.setLayout(grid)
        self.setGeometry(300, 300, 400, 100)
        self.setWindowTitle('Loading')
        self.setWindowIcon(QIcon(r'icons\icon_directory.png'))
