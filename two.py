from PyQt4 import QtGui, QtCore
import sys
import math


MAXX = 700
MAXY = 400
INCREASE = 2.0
SHRINK = 3.0
DEFAULT_STEP = 0.01

class SecondTask(QtGui.QFrame):

    def __init__(self, start, end, a):
        super(SecondTask, self).__init__()
        self.start = start
        self.end = end
        self.a = a
        self.upper_bound = 0.2
        self.step = 0.1
        self.lower_bound = 0.01
        self.setStyleSheet("background-color: rgb(255,255,255);"
                           "border:1px solid rgb(0,0,0);")

        self.initUI()

    def initUI(self):
        self.setGeometry(50, 50, MAXX, MAXY)
        self.setWindowTitle('KGG_Two')
        self.setFixedSize(MAXX, MAXY)
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawLines(event, qp)
        qp.end()

    def drawLines(self, event, qp):
        qp.setPen(QtGui.QColor(0, 0, 0))
        qp.drawLine(0, MAXY/2, MAXX, MAXY/2)
        qp.drawLine(MAXX/2, 0, MAXX/2, MAXY)

        maxx, maxy = self.resolve_minmax()
        k = min(maxx, maxy)
        qp.setPen(QtGui.QColor(150, 150, 150))
        qp.drawLine(MAXX / 2 - MAXY / 2, MAXY, MAXX / 2 + MAXY / 2, 0)
        qp.drawLine(MAXX / 2 + MAXY / 2, MAXY, MAXX / 2 - MAXY / 2, 0)
        for n in range(20):
            coords = (-0.25 *n* math.ceil(MAXY / k) + MAXX / 2, -0.25 *n* math.ceil(MAXY / k) + MAXY / 2)
            qp.drawEllipse(coords[0], coords[1],
                            0.5 *n* math.ceil(MAXY/ k), 0.5 *n* math.ceil(MAXY / k))
            qp.drawText(coords[0]+0.5 *n* math.ceil(MAXY/ k), MAXY/2, 20, 20, QtCore.Qt.AlignLeft, str(n))
            qp.drawText(MAXX/2, coords[1], 20, 20, QtCore.Qt.AlignLeft, str(n))


        qp.setPen(QtGui.QColor(0, 0, 224))
        points = self.generate_points()
        for x in range(len(points)-1):
            qp.drawLine(points[x][0]*0.25*MAXY/k + MAXX/2,
                        points[x][1]*-0.25*MAXY/k + MAXY/2,
                        points[x+1][0]*0.25*MAXY/k + MAXX/2,
                        points[x+1][1]*-0.25*MAXY/k + MAXY/2)

        qp.setPen(QtGui.QColor(255, 0, 0))
        qp.drawText(5, 5, 250, 100, QtCore.Qt.AlignLeft,
                    'r = 2^(theta/{}*pi) theta in ({}pi, {}pi)'.format(self.a, self.start, self.end))


    def resolve_borders(self, points):
        maxx = maxy = 0
        for x in points:
            if abs(x[0]) > maxx:
                maxx = abs(x[0])
            if abs(x[1]) > maxy:
                maxy = abs(x[1])

        return maxx, maxy


    def generate_points(self):
        phi = self.start*math.pi
        current_point = cartesian(phi, function(phi, self.a))
        result = [current_point]
        maxx, maxy = self.resolve_minmax()
        k = max(maxx, maxy)
        pixel_size = (2.0 * maxx / MAXX, 2.0 * maxy / MAXY)
        while phi < self.end*math.pi:
            point = cartesian(phi+self.step, function(phi+self.step, self.a))
            dist = (abs(current_point[0]-point[0]), abs(current_point[1]-point[1]))
            if dist[0] < pixel_size[0] and dist[1] < pixel_size[1]:
                self.step *= INCREASE
            elif dist[0] > pixel_size[0]*10 or dist[1] > pixel_size[1]*10:
                self.step = self.step/SHRINK
            else:
                result.append(point)
                phi += self.step
                current_point = point

        result.append(cartesian(self.end*math.pi, function(self.end*math.pi, self.a)))
        return result

    def resolve_minmax(self):
        case = self.a > 0
        interval_edge = [self.start, self.end][case]
        wholes = [math.floor(interval_edge/math.pi), math.ceil(interval_edge/math.pi)][case]
        x_border = abs(cartesian(wholes*math.pi, function(wholes*math.pi, self.a))[0])
        halves = [wholes - math.pi*0.5, wholes + math.pi*0.5][case]
        y_border = abs(cartesian(halves*math.pi, function(halves*math.pi, self.a))[1])
        return x_border, y_border

    def adjust(self, start, end, a):
        self.start = start
        self.end = end
        self.a = a


def function(phi, a):
    return math.pow(2, phi/(a*math.pi))


def cartesian(phi, r):
    return r*math.cos(phi), r*math.sin(phi)


def d(point1, point2):
    k = ((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)**0.5
    return k


def polar(x, y):
    r = (x**2 + y**2)**0.5
    phi = [math.acos(x/r), 2*math.pi - math.acos(x/r)][y < 0]
    return r, phi


def main():
    app = QtGui.QApplication(sys.argv)
    k = SecondTask(-1.0, 1.0, 2)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
