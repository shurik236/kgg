from PyQt4 import QtGui, QtCore
import sys

MAXX = 700
MAXY = 400
N = 50
M = MAXY * 3


class FifthTask(QtGui.QFrame):
    def __init__(self, a, b, c, d):
        super(FifthTask, self).__init__()
        self.x1 = a
        self.x2 = b
        self.y1 = c
        self.y2 = d
        self.min_x = 32767
        self.max_x = -32767
        self.min_y = 32767
        self.max_y = -32767
        self.top = []
        self.bottom = []
        self.upper_border = []
        self.lower_border = []
        self.transform = dimetric_transform

        for x in range(MAXX+1):
            self.upper_border.append(-1)
            self.lower_border.append(-1)

        self.resolve_minmax()
        self.points = self.generate_points()

        self.setStyleSheet("background-color: rgb(255,255,255);"
                           "border:1px solid rgb(0,0,0);")
        self.init_ui()


    def adjust(self, a, b, c, d):
        self.x1 = a
        self.x2 = b
        self.y1 = c
        self.y2 = d
        self.min_x = 32767
        self.max_x = -32767
        self.min_y = 32767
        self.max_y = -32767

    def draw(self):
        self.top = []
        self.bottom = []
        self.upper_border = []
        self.lower_border = []
        self.transform = dimetric_transform

        for x in range(MAXX + 1):
            self.upper_border.append(-1)
            self.lower_border.append(-1)

        self.resolve_minmax()
        self.points = self.generate_points()


    def init_ui(self):
        self.setGeometry(50, 50, MAXX, MAXY)
        self.setWindowTitle('KGG_Five')
        self.setFixedSize(MAXX, MAXY)
        self.show()

    def paintEvent(self, QPaintEvent):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setPen(QtGui.QColor(255, 0, 0))
        qp.drawText(5, 5, 400, 20, QtCore.Qt.AlignLeft,
                    "z = xy on [{}, {}]X[{}, {}]".format(
                        self.x1, self.x2, self.y1, self.y2))
        for x in self.points:
            if x[2]:
                qp.setPen(QtGui.QColor(0, 0, 255))
                qp.drawPoint(x[0], x[1])
            else:
                qp.setPen(QtGui.QColor(0, 255, 0))
                qp.drawPoint(x[0], x[1])
        qp.end()

    def resolve_minmax(self):
        for i in range(N+1):
            x = self.x2 + i*(self.x1-self.x2)/N
            for j in range(M+1):
                y = self.y2 + j*(self.y1-self.y2)/M
                z = func(x, y)
                xx, yy = self.transform(x, y, z)
                if xx > self.max_x:
                    self.max_x = xx
                if xx < self.min_x:
                    self.min_x = xx
                if yy > self.max_y:
                    self.max_y = yy
                if yy < self.min_y:
                    self.min_y = yy

    def generate_points(self):
        for i in range(MAXX+1):
            self.top.append(MAXY)
            self.bottom.append(0)

        for j in range(M+1):
            x = self.x2
            y = self.y2 + j*(self.y1-self.y2)/M
            z = func(x, y)

            xx, yy = self.transform(x, y, z)
            xx = round((xx - self.min_x)/(self.max_x - self.min_x)*MAXX)
            yy = round((yy - self.min_y)/(self.max_y - self.min_y)*MAXY)

            if yy < self.top[xx]:
                self.upper_border[xx] = yy

        for i in range(M+1):
            y = self.y2
            x = self.x2 + i*(self.x1-self.x2)/M
            z = func(x, y)

            xx, yy = self.transform(x, y, z)
            xx = round((xx - self.min_x) / (self.max_x - self.min_x) * MAXX)
            yy = round((yy - self.min_y) / (self.max_y - self.min_y) * MAXY)

            if yy < self.top[xx]:
                self.lower_border[xx] = yy

        for i in range(N+1):
            x = self.x2 + i*(self.x1-self.x2)/N
            for j in range(M+1):
                y = self.y2 + j*(self.y1 - self.y2)/M
                z = func(x, y)

                xx, yy = self.transform(x, y, z)
                xx = round((xx - self.min_x) / (self.max_x - self.min_x) * MAXX)
                yy = round((yy - self.min_y) / (self.max_y - self.min_y) * MAXY)

                if yy > self.bottom[xx]:
                    if i == 0 or ((self.upper_border[xx] < 0 or self.upper_border[xx] < yy) and
                                      (self.lower_border[xx] < 0 or self.lower_border[xx]< yy)):
                        yield (xx, yy, True)
                        self.bottom[xx] = yy

                if yy < self.top[xx]:
                    if i == 0 or ((self.upper_border[xx] < 0 or self.upper_border[xx] >= yy) and
                                      (self.lower_border[xx] < 0 or self.lower_border[xx] >= yy)):
                        yield (xx, yy, False)
                        self.top[xx] = yy

        for j in range(MAXX):
            self.top[j] = MAXX
            self.bottom[j] = 0

        for j in range(N+1):
            y = self.y2 + j*(self.y1 - self.y2)/N
            for i in range(M+1):
                x = self.x2 + i*(self.x1 - self.x2)/M
                z = func(x, y)

                xx, yy = self.transform(x, y, z)
                xx = round((xx - self.min_x) / (self.max_x - self.min_x) * MAXX)
                yy = round((yy - self.min_y) / (self.max_y - self.min_y) * MAXY)

                if yy > self.bottom[xx]:
                    if i == 0 or ((self.upper_border[xx] < 0 or self.upper_border[xx] < yy) and
                                      (self.lower_border[xx] < 0 or self.lower_border[xx]< yy)):
                        yield (xx, yy, True)
                        self.bottom[xx] = yy

                if yy < self.top[xx]:
                    if i == 0 or ((self.upper_border[xx] < 0 or self.upper_border[xx] >= yy) and
                                      (self.lower_border[xx] < 0 or self.lower_border[xx] >= yy)):
                        yield (xx, yy, False)
                        self.top[xx] = yy


def func(x, y):
    return x*y


def dimetric_transform(x, y, z):
    return -x/(2*1.414) + y, x/(2*1.414) - z


def isometric_transform(x, y, z):
    return (y-x)*1.732, (x+y)/2 - z


def main():
    app = QtGui.QApplication(sys.argv)
    k = FifthTask(-10, 10, -10, 10)
    sys.exit(app.exec_())

if __name__ == '__main__':
    pass
