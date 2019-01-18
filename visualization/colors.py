
class Colors:
    def __init__(self):
        self.filename = 'colors.txt'

    def get_colors(self):
        colors = list()
        with open(self.filename) as f:
            f = f.readlines()
            for line in f:
                colors.append(line.replace('\n', ''))
        return colors
