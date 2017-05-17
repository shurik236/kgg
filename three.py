from PyQt4 import QtCore, QtGui
import itertools
import sys
import math


MAXX = 700
MAXY = 400
DELTAS_1 = [0, 1]
DELTAS_2 = [-1, 0]


class ThirdTask(QtGui.QFrame):

    def __init__(self, a, b, x_size, y_size):
        super(ThirdTask, self).__init__()
        self.a = a
        self.x_size = x_size
        self.y_size = y_size

        self.setStyleSheet("background-color: rgb(255,255,255);"
                           "border:1px solid rgb(0,0,0);")
        self.init_ui()

    def init_ui(self):
        self.setGeometry(50, 50, MAXX, MAXY)
        self.setWindowTitle('KGG_Three')
        self.setFixedSize(MAXX, MAXY)
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.draw_grid(event, qp)
        self.draw_legend(event, qp)
        self.draw_directress(event, qp)
        if self.x_size < 1 and self.y_size < 1:
            self.draw_closeup(event, qp)
        else:
            self.draw_lines(event, qp)
        qp.end()

    def draw_lines(self, event, qp):
        qp.setPen(QtGui.QColor(0, 0, 255))
        points = self.generate_points()
        for pt in points:
            qp.drawPoint(pt[0], pt[1])

    def draw_closeup(self, event, qp):
        qp.setPen(QtGui.QColor(0, 0, 255))
        qp.setBrush(QtGui.QColor(0, 0, 255))
        points = self.generate_points()
        for k in range(0, len(points)):
            qp.drawRect(points[k][0], points[k][1], 3, 3)


    def draw_legend(self, event, qp):
        qp.setPen(QtGui.QColor(255, 0, 0))
        qp.drawText(5, 5, 400, 20, QtCore.Qt.AlignLeft,
                    "y^2 = {}x on [-{}, {}] X [-{}, {}]".format(
                        self.a * 2, self.x_size, self.x_size, self.y_size, self.y_size))

    def draw_grid(self, event, qp):
        # axes
        qp.setPen(QtGui.QColor(0, 0, 0))
        qp.drawLine(0, MAXY / 2, MAXX, MAXY / 2)
        qp.drawLine(MAXX / 2, 0, MAXX / 2, MAXY)
        qp.drawText(MAXX / 2, MAXY / 2, 20, 20, QtCore.Qt.AlignLeft, "0")

        qp.setPen(QtGui.QColor(150, 150, 150))
        x_grid, y_grid = self.generate_grid()
        for xn in x_grid:
            qp.drawLine(xn, 0, xn, MAXY)
            qp.drawText(xn, MAXY/2, 50, 20, QtCore.Qt.AlignLeft, str(x_grid[xn]))
        for yn in y_grid:
            qp.drawLine(0, yn, MAXX, yn)
            qp.drawText(MAXX/2, yn, 50, 20, QtCore.Qt.AlignLeft, str(y_grid[yn]))

    def draw_directress(self, event, qp):
        qp.setPen(QtGui.QColor(255, 0, 0))
        directress = self.converted(-self.a/2, 0)[0]
        focal_axis = self.converted(self.a/2, 0)[0]
        qp.drawLine(directress, 0, directress, MAXY)
        qp.drawText(directress, MAXY/2, 100, 20, QtCore.Qt.AlignLeft, str(-self.a/2))
        qp.drawLine(focal_axis, 0, focal_axis, MAXY)
        qp.drawText(focal_axis, MAXY / 2, 100, 20, QtCore.Qt.AlignLeft, str(self.a / 2))

    def converted(self, x, y):
        pixel_size = 2*self.x_size/MAXX, 2*self.y_size/MAXY
        zero_point = MAXX/2, MAXY/2
        return int(x/pixel_size[0] + zero_point[0]), int(y/pixel_size[1] + zero_point[1])

    def reverse_converted(self, x, y):
        pixel_size = 2*self.x_size/MAXX, 2*self.y_size/MAXY
        zero_point = MAXX/2, MAXY/2
        return (x - zero_point[0])*pixel_size[0], (y - zero_point[1])*pixel_size[1]

    def generate_points(self):
        points = []
        scale = 1
        if self.x_size < 1 and self.y_size < 1:
            scale = 3
        focus = (self.a/2, 0)
        current_x, current_y = self.converted(0, 0)
        points.append((current_x, current_y))
        while current_x < MAXX and current_y > 0:
            neighbor = itertools.product(DELTAS_1, DELTAS_2)
            least_difference = 100500
            current_shift = (0, 0)
            for pt in neighbor:
                if pt == (0, 0):
                    continue
                f_dist = distance(self.reverse_converted(current_x + pt[0]*scale, current_y + pt[1]*scale), focus)
                d_dist = self.reverse_converted(current_x + pt[0]*scale, current_y + pt[1]*scale)[0] - (-self.a/2)
                difference = abs(f_dist - d_dist)
                if difference < least_difference:
                    least_difference = difference
                    current_shift = pt

            current_x += current_shift[0]*scale
            current_y += current_shift[1]*scale
            points.append((current_x, current_y))

            #points.append((current_x, MAXY - current_y))

        for k in range(len(points)):
            points.append((points[k][0], MAXY - points[k][1]))

        return points

    def generate_grid(self):
        x_grid = {}
        y_grid = {}
        x_step = math.ceil(self.x_size/10)
        y_step = math.ceil(self.y_size/10)
        for n in range(math.ceil(self.x_size)):
            cell = self.converted((n+1)*x_step, 0)
            x_grid[cell[0]] = (n+1)*x_step
            x_grid[MAXX - cell[0]] = -(n+1)*x_step
        for n in range(math.ceil(self.y_size)):
            cell = self.converted(0, (n+1)*y_step)
            y_grid[cell[1]] = -(n+1)*y_step
            y_grid[MAXY - cell[1]] = (n+1)*y_step

        return x_grid, y_grid

    def adjust(self, a, x_size, y_size):
        self.a = a
        self.x_size = x_size
        self.y_size = y_size


def distance(point_a, point_b):
    return ((point_a[0]-point_b[0])**2 + (point_a[1]-point_b[1])**2)**0.5


def main():
    app = QtGui.QApplication(sys.argv)
    k = ThirdTask(2, 2, 10, 10)
    sys.exit(app.exec_())


if __name__ == '__main__':
    pass
