from PyQt4 import QtGui, QtCore
import sys


MAXX = 696
MAXY = 360
LIMIT = 1500


class FirstTask(QtGui.QFrame):

    def __init__(self, start, end, a, b):
        super(FirstTask, self).__init__()

        self.start = start
        self.end = end
        self.a = a
        self.b = b
        self.setStyleSheet("background-color: rgb(255,255,255);"
                                  "border:1px solid rgb(0,0,0);")
        self.initUI()

    def adjust(self, start, end, a, b):
        self.start = start
        self.end = end
        self.a = a
        self.b = b

    def initUI(self):
        self.setGeometry(50, 50, 696, 360)
        self.setFixedSize(696, 360)

        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        axes = generate_axes(self.start, self.end, self.a, self.b)
        points = generate_points(self.start, self.end, self.a, self.b)
        self.drawLines(event, qp, points, axes)
        qp.end()

    def drawLines(self, event, qp, points, axes):
        qp.setPen(QtGui.QColor(0, 0, 0))
        ax, ay = axes
        if ax>=0:
            qp.drawLine(ax, 0, ax, MAXY)
        if ay>=0:
            qp.drawLine(0, MAXY - ay, MAXX, MAXY - ay)

        qp.setPen(QtGui.QColor(0, 0, 255))
        for i in range(1, MAXX):
            p1 = points[i]
            p0 = points[i-1]
            if p0[1] == p1[1] == 0:
                continue
            qp.drawLine(p0[0], p0[1], p1[0], p1[1])

        qp.setPen(QtGui.QColor(255, 0, 0))
        qp.drawText(5, 5, 250, 100, QtCore.Qt.AlignLeft,
                    'y=((x+{0})/({1}-x))**4 on ({2}, {3})'.format(self.a, self.b, self.start, self.end))


def function(x, a, b):
    if b==x:
        return LIMIT
    else:
        result = ((x+a)/(b-x))**4
        #result = math.sin(x)
        if abs(result) >= LIMIT:
            return LIMIT
        else:
            return result


def generate_minmax(start, end, a, b):
    ymin = function(start, a, b)
    ymax = function(start, a, b)
    for xx in range(MAXX):
        x = start + (xx*(end-start))/(MAXX)
        y = function(x, a, b)
        if (y < ymin):
            ymin = y
        if (y > ymax):
            ymax = y

    return ymin-(ymax-ymin)/10.0, ymax-(ymax-ymin)/10.0


def generate_axes(start, end, a, b):
    if start*end < 0:
        x = abs(start)*MAXX/(end - start)
    else:
        x = -1
    ymin, ymax = generate_minmax(start, end, a, b)
    if ymin*ymax < 0:
        y = (MAXY)*abs(ymin)/(ymax - ymin)
    else:
        y = -1

    return x, y


def generate_points(start, end, a, b):
    result = []
    ymin, ymax = generate_minmax(start, end, a, b)
    for xx in range(MAXX):
        x = start + (xx*(end-start))/MAXX
        y = function(x, a, b)
        yy = (y-ymax)*(MAXY)/(ymin-ymax)
        result.append((xx, yy))

    return result


def main():
    app = QtGui.QApplication(sys.argv)
    k = FirstTask(5, 6, 2, 3)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
