from PyQt5.QtWidgets import QWidget,\
    QGridLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon


class Editor(QWidget):
    def __init__(self, graph, func_for_click):
        super().__init__()
        self.graph = graph
        self.func_for_click = func_for_click
        self.create_gui()

    def create_gui(self):
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self._i = 0
        self.labels = dict()
        for vertex in self.graph.vertices:
            number_of_country = QLabel('Country ' + str(self._i + 1))
            regions = dict()
            for j in range(len(vertex.regions)):
                regions.update({j: vertex.regions[j].points})
            regions = QLineEdit(str(regions))
            self.labels[number_of_country] = regions
            self.grid.addWidget(number_of_country, self._i, 0)
            self.grid.addWidget(regions, self._i, 1)
            self._i += 1
        button_edit = QPushButton('Edit')
        button_edit.clicked.connect(self.func_for_click)
        self.grid.addWidget(button_edit, self._i+1, self._i+1)

        button_add = QPushButton('Add Country')
        button_add.clicked.connect(self.add_country)
        self.grid.addWidget(button_add, self._i+1, self._i)
        self.setLayout(self.grid)
        self.setGeometry(300, 300, 550, 500)
        self.setWindowTitle('Country Editor')
        self.setWindowIcon(QIcon(r'icons\icon_brush.png'))

    def add_country(self):
        number_of_country = QLabel('Country ' + str(self._i + 1))
        regions = QLineEdit()
        self.labels[number_of_country] = regions
        self.grid.addWidget(number_of_country, self._i, 0)
        self.grid.addWidget(regions, self._i, 1)
        self._i += 1
