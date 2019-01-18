import argparse
from parser_countries import Parser
from graph.graph import Graph, CountryVertex
from graph.graph_generator import Generator
from PyQt5.QtWidgets import QApplication
from visualization.map_window import MapWindow
import sys


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--countries', '-c', default='',
                       help='Enter the counties.'
                            'Countries are separated of figure brackets.'
                            'Regions in countries are separated '
                            'of square brackets.'
                            'Points in regions are separated '
                            'of circle brackets.'
                            'MENU is menu of actions.'
                            'SAVE is to save map in file.'
                            'LOAD is to load map from file.'
                            'EDIT MAP is to edit map in two modes.'
                            'First mode is online.'
                            'Second mode is dynamic.'
                            'TOOLS is for choose color of pen.')
    group.add_argument('--generate', '-g', type=int, default=0,
                       help='Enter the wanted count of colors.'
                            'Count should be positive.'
                            'Default is zero.')

    args = parser.parse_args()
    graph = Graph(list())
    vertices = list()
    scale = 1
    if args.generate < 0:
        raise ValueError('Count of generate should be positive')
    if args.countries != '':
        tree = Parser(args.countries).get_tree()
        for country in tree:
            if isinstance(country, list):
                vertices.append(CountryVertex(country[1], country[0]))
            else:
                vertices.append(CountryVertex(country))
        graph = Graph(vertices)
    if args.generate != 0:
        generator = Generator(int(args.generate))
        graph = generator.generate_map()
        scale = 6
    app = QApplication(sys.argv)
    window = MapWindow(graph)
    if args.countries != '' or args.generate != 0:
        window.draw_map()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
