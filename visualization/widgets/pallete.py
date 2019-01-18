from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage, QPainter, QPen, QBrush, QColor, QIcon
from math import floor


class Palette(QWidget):
    def __init__(self, colors, image_painter, func_for_click, func_for_press):
        super().__init__()
        self.colors = colors
        lenght_colors = len(self.colors)
        self.setFixedSize(120, lenght_colors//4*30)
        self.image = QImage(self.width(), self.height(), QImage.Format_ARGB32)
        self.painter = image_painter
        self.func_for_click = func_for_click
        self.func_for_press = func_for_press
        self._current_color = None
        self.setWindowTitle('Palette')
        self.setWindowIcon(QIcon(r'icons\icon_palette.png'))
        self.draw_colors()

    def draw_colors(self):
        painter = QPainter(self.image)
        index = 0
        self.poitions = dict()
        for i in range(4):
            for j in range(len(self.colors)//4):
                self.poitions[(i, j)] = self.colors[index]
                painter.setPen(QPen(QColor(self.colors[index])))
                painter.setBrush(QBrush(QColor(self.colors[index])))
                painter.drawRect(i*30, j*30, 30, 30)
                index += 1

    def mousePressEvent(self, QMouseEvent):
        pos = QMouseEvent.pos()
        x = floor(pos.x()/30)
        y = floor(pos.y()/30)
        self._current_color = self.poitions[(x, y)]
        self.painter.setPen(QPen(QColor(self._current_color)))
        self.painter.setBrush(QBrush(QColor(self._current_color)))
        self.func_for_press()
        self.func_for_click()

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)
