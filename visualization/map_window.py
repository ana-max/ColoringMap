from PyQt5.QtWidgets import QMainWindow, QAction, QMenu, QDesktopWidget
from PyQt5.QtGui import QImage, QPainter, QPen, QColor, QIcon
from PyQt5.QtCore import Qt
from graph.graph import Graph, CountryVertex
from graph.polygon import Polygon
from collections import namedtuple
from visualization.widgets.pallete import Palette
from visualization.widgets.editor import Editor
from visualization.widgets.saver_and_loader import Saver, Loader
import json
import math
Point = namedtuple('Point', 'x y')


class MapWindow(QMainWindow):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        self.colors = graph.colors
        self.setMouseTracking(True)
        self.cp = QDesktopWidget().availableGeometry()
        self.resize(self.cp.width()-50, self.cp.height()-50)
        self.image = QImage(self.width(), self.height(), QImage.Format_ARGB32)
        self.image_painter = QPainter(self.image)
        self.image_painter.setPen(QPen(QColor(Qt.black), 2))
        self._pen_is_black = True
        self.image.fill(Qt.white)
        self.palette = Palette(self.colors, self.image_painter,
                               self.repaint, self.palette_click)
        self.is_double_press = False
        self.saver = Saver(self.save_to_file)
        self.loader = Loader(self._load_from_file)
        self.editor = Editor(self.graph, self._edit_countries)
        self._is_edit_mode = False
        self._is_delete_point_mode = False
        self._is_adding_point_mode = False
        self._is_adding_new_country_mode = False
        self._is_choose_country_mode = False
        self._regions_count = -1
        self._get_size_of_map()
        self.init_UI()

    def init_UI(self):
        self.menu = QMenu('Menu', self)
        save_to_file = QAction('Save to file', self)
        save_to_file.triggered.connect(self._saver_show)
        self.menu.addAction(save_to_file)
        load_from_file = QAction('Load from file', self)
        load_from_file.triggered.connect(self._loader_show)
        self.menu.addAction(load_from_file)
        edit_map = QMenu('Edit map', self)
        edit_online = QMenu('Edit online', self)
        edit_dynamic = QAction('Edit dynamic', self)
        edit_dynamic.triggered.connect(self._editor_show)

        add_country = QAction('Add new country', self)
        add_country.triggered.connect(self._add_country)

        delete_points = QAction('Delete points in old country', self)
        delete_points.triggered.connect(self._delete_points)

        add_points = QAction('Add points in old region', self)
        add_points.triggered.connect(self._add_points)

        edit_online.addAction(add_country)
        edit_online.addAction(delete_points)

        edit_map.addMenu(edit_online)
        edit_map.addAction(edit_dynamic)
        self.menu.addMenu(edit_map)
        self.menuBar().addMenu(self.menu)
        self.tools = QMenu('Tools', self)
        palette = QAction('Choose color', self)
        palette.triggered.connect(
            self.palette.show)
        self.tools.addAction(palette)

        self.save = QAction('Save Country')
        self.save.triggered.connect(self._save_country)

        self.pour = QAction('Pour')
        self.pour.triggered.connect(self._pour)

        self.add_region = QAction('Add Region')
        self.add_region.triggered.connect(self._add_region)

        self.stop = QAction('Stop Delete')
        self.stop.triggered.connect(self._stop_delete)

        self.choose_country = QAction('Сhoose country')
        self.choose_country.triggered.connect(self._choose_country)

        self.stop_add_points = QAction('Stop add')
        self.stop_add_points.triggered.connect(self._stop_adding)

        self.menuBar().addMenu(self.menu)
        self.menuBar().addMenu(self.tools)
        self.menuBar().addAction(self.save)
        self.menuBar().addAction(self.pour)
        self.menuBar().addAction(self.add_region)
        self.menuBar().addAction(self.stop)
        self.change_menu_bar()
        self.setWindowTitle('Python Coloring Map')
        self.setWindowIcon(QIcon(r'icons\icon_pencils.png'))

    def change_menu_bar(self):
        if self._is_adding_new_country_mode:
            self.save.setVisible(True)
            self.pour.setVisible(True)
            self.add_region.setVisible(True)
            self.menu.setDisabled(True)
            self.stop.setVisible(False)
        elif self._is_delete_point_mode:
            self.stop.setVisible(True)
            self.save.setVisible(False)
            self.add_region.setVisible(False)
            self.pour.setVisible(False)
            self.menu.setDisabled(True)
            self.tools.setDisabled(True)
        elif self._is_adding_point_mode:
            self.stop.setVisible(False)
            self.save.setVisible(False)
            self.add_region.setVisible(False)
            self.pour.setVisible(False)
            self.menu.setDisabled(True)
            self.tools.setDisabled(True)
        else:
            self.menu.setEnabled(True)
            self.tools.setEnabled(True)
            self.save.setVisible(False)
            self.add_region.setVisible(False)
            self.pour.setVisible(False)
            self.stop.setVisible(False)

    def palette_click(self):
        self._pen_is_black = False

    def _add_points(self):
        self._on_edit_mode()
        self._is_adding_point_mode = True
        self.change_menu_bar()

    def _choose_country(self):
        self._is_choose_country_mode = True
        self.change_menu_bar()

    def _stop_adding(self):
        self._is_adding_point_mode = True
        self._is_edit_mode = False
        self.change_menu_bar()
        self.repaint()

    def _delete_points(self):
        self._on_edit_mode()
        self._is_delete_point_mode = True
        self.change_menu_bar()

    def _stop_delete(self):
        self._is_delete_point_mode = False
        self._is_edit_mode = False
        self.change_menu_bar()
        self.repaint()

    def _add_country(self):
        self._on_edit_mode()
        self._is_adding_new_country_mode = True
        self.graph.add_vertex(CountryVertex([]))
        self.graph.vertices[-1].regions = dict()
        self._add_region()
        self.change_menu_bar()

    def _add_region(self):
        self._regions_count += 1
        self._is_adding_region_mode = True
        self.graph.vertices[-1].regions\
            .update({self._regions_count: Polygon(list())})

    def _save_country(self):
        self._is_adding_new_country_mode = False
        self.palette._current_color = None
        self.statusBar().showMessage('')
        self._regions_count = -1
        self.image_painter.setPen(QPen(QColor(Qt.black), 2))
        self._pen_is_black = True
        self.change_menu_bar()

    def _pour(self):
        if self.palette._current_color is not None:
            self.graph.vertices[-1].color = \
                self.palette._current_color
            self.palette._current_color = None
            if self.palette._current_color in self.graph.colors:
                self.graph.colors.remove(self.palette._current_color)
        self.image.fill(Qt.white)
        self.draw_map()
        self.repaint()

    def _on_edit_mode(self):
        self._is_edit_mode = True
        self.statusBar().showMessage('Online Edit Map')

    def repaint_key(self):
        self.image.fill(Qt.white)
        self.draw_map()
        self.repaint()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Plus:
            self.scale += 1
            self.repaint_key()
            self.repaint()
        if event.key() == Qt.Key_Minus:
            self.scale -= 1
            self.repaint_key()
        if event.key() == Qt.Key_Right:
            self.shift_x += 1
            self.repaint_key()
        if event.key() == Qt.Key_Left:
            self.shift_x -= 1
            self.repaint_key()
        if event.key() == Qt.Key_Up:
            self.shift_y -= 1
            self.repaint_key()
        if event.key() == Qt.Key_Down:
            self.shift_y += 1
            self.repaint_key()

    def find_point_on_the_map(self, point):
        min_d = 100000000
        needed_point = 0
        country = 100
        number_region = 100
        for vertex in self.graph.vertices:
            for region in vertex.regions:
                if vertex.regions[region].point_in_polygon(point):
                    for p in vertex.regions[region].points:
                        x = point.x - p.x
                        y = point.y - p.y
                        dim = math.sqrt(x ** 2 + y ** 2)
                        if dim < min_d:
                            min_d = dim
                            needed_point = p
                            number_region = region
                            country = vertex
        return country, number_region, needed_point

    def delete_point(self, point):
        country, number_region, needed_point = self\
            .find_point_on_the_map(point)
        for vertex in self.graph.vertices:
            if vertex == country:
                vertex.regions[number_region].points.remove(needed_point)
                region = vertex.regions[number_region]
                if len(region.points) == 2:
                    vertex.regions[number_region].points = list()
        self.image.fill(Qt.white)
        self.draw_map()
        self.repaint()

    def mousePressEvent(self, mouse_event):
        sup_x = - self.shift_x
        sup_y = - self.shift_y
        x = int((mouse_event.x() + sup_x) / self.scale)
        y = int(-(mouse_event.y() + sup_y) / self.scale)
        if self._is_delete_point_mode:
            self.delete_point(Point(x, y))
        if self._is_edit_mode and not self._is_delete_point_mode:
            if self._is_adding_new_country_mode:
                point = Point(x, y)
                if point not in \
                        self.graph.vertices[-1]\
                            .regions[self._regions_count].points:
                    self.graph.vertices[-1].regions[self._regions_count]\
                        .points.append(point)
            if not self.is_double_press:
                self.mouse_pos = mouse_event.pos()
            self.image_painter\
                .drawPoint(self.mouse_pos.x(), self.mouse_pos.y())
            self.repaint()

    def mouseDoubleClickEvent(self, mouse_event):
        if self._is_edit_mode:
            if not self.is_double_press:
                self.is_double_press = True
            else:
                self.is_double_press = False
                self.image_painter\
                    .drawLine(self.mouse_pos.x(), self.mouse_pos.y(),
                              self.now_mouse_pos.x(), self.now_mouse_pos.y())
                self.repaint()
            self.mousePressEvent(mouse_event)

    def mouseMoveEvent(self, mouse_event):
        self.now_mouse_pos = mouse_event.pos()
        if self._is_edit_mode:
            if self.is_double_press:
                self.repaint()

    def save_to_file(self):
        file_name = self.saver.save_edit.text()
        with open(file_name, 'w') as f:
            for vertex in self.graph.vertices:
                for region in vertex.regions:
                    vertex.regions[region] =\
                        vertex.regions[region].points
                f.write(json.dumps(vertex.regions))
                f.write('\n')
        self.saver.close()

    def parse_file(self, load):
        sup_regions = []
        regions = dict()
        for l in load:
            for region in load[l]:
                r = Point(region[0], region[1])
                sup_regions.append(r)
            regions[int(l)] = Polygon(sup_regions.copy())
            sup_regions.clear()
        return regions

    def _repaint_load(self, vertices):
        self.graph = Graph(vertices)
        self.saver = Saver(self.save_to_file)
        self.loader = Loader(self._load_from_file)
        self.editor = Editor(self.graph, self._edit_countries)
        self.colors = self.graph.colors
        self.image.fill(Qt.white)
        self.coloring = [dict(), 0]
        self.is_double_press = False
        self._get_size_of_map()
        self.draw_map()
        self.repaint()

    def _load_from_file(self):
        filename = self.loader.load_edit.text()
        vertices = list()
        loads = list()
        index = 0
        countries = dict()
        with open(filename, 'r') as f:
            for line in f:
                load = json.loads(line)
                if load != '':
                    loads.append(self.parse_file(load))
                    countries[index] = loads[0]
                    index += 1
                    loads.clear()
        for country in countries:
            vertices.append(CountryVertex(countries[country]))
        self.loader.close()
        self._repaint_load(vertices)

    def _get_size_of_map(self):
        min_map_x = min_map_y = 10000000
        max_map_x = max_map_y = 0
        for vertex in self.graph.vertices:
            for polygon in vertex.regions:
                min_x, min_y, max_x, max_y = self.\
                    _find_wrapper_polygon(vertex.regions[polygon])
                if min_x < min_map_x:
                    min_map_x = min_x
                if min_y < min_map_y:
                    min_map_y = min_y
                if max_x > max_map_x:
                    max_map_x = max_x
                if max_y > max_map_y:
                    max_map_y = max_y
        map_width = max_map_x - min_map_x
        map_height = max_map_y - min_map_y
        scale_width = self.width()//map_width
        scale_height = (self.height()-100)//map_height
        scale = min(scale_width, scale_height)
        if scale <= 0:
            self.image.scaled(map_width, map_height)
        self.shift_x = 0
        self.shift_y = 0
        offset_x = self.image.width()//2 - map_width*scale//2
        if min_map_x*scale < 0:
            self.shift_x = abs(min_map_x*scale) + offset_x
        if min_map_y*-scale > self.image.height():
            self.shift_y = -(min_map_y*-scale - self.image.height() + 50)
        if max_map_x*scale > self.image.width():
            self.shift_x = -(max_map_x*scale - self.image.width())
        if max_map_y*-scale < 0:
            self.shift_y = abs(max_map_y*-scale) + 50
        self.scale = scale

    def _edit_countries(self):
        vertices = list()
        for label in self.editor.labels:
            if self.editor.labels[label].text() != '':
                dict_of_vertex = eval(self.editor.labels[label].text())
                for key in dict_of_vertex:
                    dict_of_vertex[key] = Polygon(dict_of_vertex[key])
                vertices\
                    .append(CountryVertex(dict_of_vertex))
        self._repaint_load(vertices)

    def _saver_show(self):
        self.saver.show()

    def _loader_show(self):
        self.loader.show()

    def _editor_show(self):
        self.editor.show()

    def draw_circuit(self, region):
        for i in range(len(region.points)-1):
            self.image_painter.setPen(QPen(QColor(Qt.black), 2))
            self._pen_is_black = True
            point1 = region.points[i]
            point2 = region.points[i + 1]
            x1, y1 = self.scaled_point(point1)
            x2, y2 = self.scaled_point(point2)
            self.image_painter\
                .drawLine(x1, y1, x2, y2)
            first = region.points[0]
            last = region.points[-1]
            x1, y1 = self.scaled_point(first)
            x2, y2 = self.scaled_point(last)
            self.image_painter \
                .drawLine(x1, y1, x2, y2)

    def scaled_point(self, point):
        x = point.x*self.scale + self.shift_x
        y = point.y*-self.scale + self.shift_y
        return x, y

    def scaled_region(self, region):
        new_region = list()
        for point1 in region.points:
            p = Point(point1.x*self.scale + self.shift_x,
                      point1.y*-self.scale + self.shift_y)
            new_region.append(p)
        return Polygon(new_region)

    def _find_wrapper_polygon(self, region):
        min_x = min_y = 1000000000
        max_x = max_y = 0
        for point in region.points:
            if point.x < min_x:
                min_x = point.x
            if point.x > max_x:
                max_x = point.x
            if point.y < min_y:
                min_y = point.y
            if point.y > max_y:
                max_y = point.y
        return min_x, min_y, max_x, max_y

    def draw_map(self):
        self.graph.coloringGraph()
        for vertex in self.graph.vertices:
            for region in vertex.regions:
                self.fill_region(vertex.regions[region], vertex.color)
                self.draw_circuit(vertex.regions[region])

    def fill_region(self, region, color):
        new_region = self.scaled_region(region)
        min_x, min_y, max_x, max_y = self._find_wrapper_polygon(new_region)
        difference_y = max_y - min_y
        difference_x = max_x - min_x
        for i in range(difference_y):
            self.coloring_line(new_region,
                               Point(min_x, max_y - i), difference_x, color)

    def coloring_line(self, region, start, difference_x, color):
        color = QColor(color)
        for i in range(difference_x):
            if region.point_in_polygon(Point(start.x+i, start.y)):
                pixel_color = QColor(self.image.pixel(start.x+i, start.y))
                if pixel_color != QColor(Qt.white):
                    self.image_painter.setPen(QPen(Qt.white))
                    self.image_painter.drawPoint(start.x+i, start.y)
                    pixel_color.setAlpha(255//2)
                    self.image_painter.setPen(QPen(pixel_color))
                    self.image_painter.drawPoint(start.x+i, start.y)
                    color.setAlpha(255//2)
                self._pen_is_black = False
                self.image_painter.setPen(QPen(color))
                self.image_painter.drawPoint(start.x+i, start.y)
                color.setAlpha(255)

    def paintEvent(self, event):
        self.image.scaled(self.width(), self.height(), Qt.KeepAspectRatio)
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)
        if self.is_double_press:
            painter.setPen(self.image_painter.pen())
            painter.drawLine(self.mouse_pos.x(),
                             self.mouse_pos.y(),
                             self.now_mouse_pos.x(),
                             self.now_mouse_pos.y())
