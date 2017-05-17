from PyQt4 import QtGui, QtCore
import sys
import assistance
import copy
import math


MAXX = 700
MAXY = 400


class FourthTask(QtGui.QFrame):

    def __init__(self):
        super(FourthTask, self).__init__()
        self.a_complete = False
        self.b_complete = False
        self.clipped = False
        self.polygon_count = 0

        self.polygon_a = []
        self.polygon_b = []
        self.intersections = set()
        self.no_intersections = True

        self.setStyleSheet("background-color: rgb(255,255,255);"
                           "border:1px solid rgb(0,0,0);")
        self.init_ui()

    def mousePressEvent(self, QMouseEvent):
        self.click_handler(QMouseEvent)


    def init_ui(self):
        self.setGeometry(50, 50, MAXX, MAXY)
        self.setWindowTitle('KGG_Four')
        self.setFixedSize(MAXX, MAXY)

        self.show()

    def paint_polygon(self, event, qp, polygon):
        for k in range(len(polygon)):
            qp.drawRect(polygon[k][0] - 2, polygon[k][1] - 2, 5, 5)
            if k > 0:
                line = assistance.draw_line(polygon[k-1], polygon[k])
                for l in line:
                    qp.drawPoint(l[0], l[1])

    def fill_polygon(self, event, qp, polygon, density):
        max_y = max([p[1] for p in polygon])
        min_y = min([p[1] for p in polygon])
        max_x = max([p[0] for p in polygon])
        min_x = min([p[0] for p in polygon])

        for y in range(min_y+1, max_y, density):
            intersections = []
            #special_point = polygon[0][0]
            for k in range(len(polygon)-1):
                i = intersect_segments((min_x, y), (max_x, y), polygon[k], polygon[k+1])
                if i:
                    '''and not (i == special_point and i in intersections)'''
                    intersections.append(i[0])
            intersections = sorted(intersections)
            for k in range(0, len(intersections)-1):
                for x in range(intersections[k], intersections[k+1]):
                    if check_polygon(polygon, (x, y)):
                        qp.drawPoint(x, y)

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setPen(QtGui.QColor(255, 0, 0))
        qp.drawText(5, 5, 600, 20, QtCore.Qt.AlignLeft,
                    'Draw two convex polygons. Click \"Clip\" to see their symmetrical difference.')
        qp.setPen(QtGui.QColor(0, 0, 255))
        qp.setBrush(QtGui.QColor(0, 0, 255))
        self.paint_polygon(event, qp, self.polygon_a)
        qp.setPen(QtGui.QColor(0, 255, 0))
        qp.setBrush(QtGui.QColor(0, 255, 0))
        self.paint_polygon(event, qp, self.polygon_b)

        qp.setPen((QtGui.QColor(255, 0, 0)))
        if self.a_complete and self.b_complete and self.clipped:
            if not self.no_intersections:
                self.paint_polygon(event, qp, self.symmetrical_difference())
                self.fill_polygon(event, qp, self.symmetrical_difference(), 2)
            else:
                for polygon in self.union():
                    self.paint_polygon(event, qp, polygon)
                    self.fill_polygon(event, qp, polygon, 2)
                qp.setPen(QtGui.QColor(255, 255, 255))
                for polygon in self.intersection():
                    self.paint_polygon(event, qp, polygon)
                    self.fill_polygon(event, qp, polygon, 1)


        qp.end()


    def click_handler(self, e):
        if self.polygon_count > 1:
            return
        next_point = (e.pos().x(), e.pos().y())
        if self.polygon_count:
            polygon = self.polygon_b
        else:
            polygon = self.polygon_a
        if len(polygon) == 0:
            polygon.append(next_point)
        else:
            dist = assistance.squared_distance(next_point, polygon[0])
            if dist < 20:
                polygon.append(polygon[0])
                if self.polygon_count:
                    self.b_complete = True
                else:
                    self.a_complete = True
                self.polygon_count += 1
            else:
                polygon.append(next_point)
        self.update()

    def clear(self):
        self.a_complete = False
        self.b_complete = False
        self.no_intersections = True
        self.intersections = set()
        self.clipped = False
        self.polygon_a = []
        self.polygon_b = []
        self.polygon_count = 0

    def clip(self):
        if self.polygon_count != 2:
            return

        self.fill_intersections()

        self.polygon_a = sort_clockwise(self.polygon_a)
        self.polygon_b = sort_clockwise(self.polygon_b)

        print('polygon a: ', self.polygon_a)
        print('polygon b: ', self.polygon_b)

        self.clipped = True


    def fill_intersections(self):
        new_polygon_a = copy.deepcopy(self.polygon_a)
        new_polygon_b = copy.deepcopy(self.polygon_b)
        a_index = 0
        b_index = 0
        for k in range(len(self.polygon_a)-1):
            for l in range(len(self.polygon_b)-1):
                i = intersect_segments(self.polygon_a[k],
                                       self.polygon_a[k+1],
                                       self.polygon_b[l],
                                       self.polygon_b[l+1])
                if i:
                    self.no_intersections = False
                    new_polygon_a.insert(a_index+1, i)
                    self.intersections.add(i)
                    a_index += 1
            a_index += 1

        for k in range(len(self.polygon_b)-1):
            for l in range(len(self.polygon_a)-1):
                i = intersect_segments(self.polygon_a[l],
                                       self.polygon_a[l + 1],
                                       self.polygon_b[k],
                                       self.polygon_b[k + 1])
                if i:
                    self.no_intersections = False
                    new_polygon_b.insert(b_index+1, i)
                    b_index += 1
            b_index += 1

        self.polygon_a = new_polygon_a
        self.polygon_b = new_polygon_b

    def union(self):
        if self.no_intersections:
            if check_polygon(self.polygon_b, self.polygon_a[0]):
                return [self.polygon_b]
            if check_polygon(self.polygon_a, self.polygon_b[0]):
                return [self.polygon_a]
            else:
                return [self.polygon_a, self.polygon_b]

        k = 0
        union = []
        current_polygon = 0
        polygons = [self.polygon_a[0: -1], self.polygon_b[0: -1]]
        while check_polygon(self.polygon_b, self.polygon_a[k]):
            k += 1
        start = polygons[current_polygon][k]
        union.append(start)
        k = (k + 1)%(len(polygons[current_polygon]))

        while polygons[current_polygon][k] != start:
            current_vertex = polygons[current_polygon][k]
            if current_vertex in self.intersections:
                k = find_index(current_vertex,
                               polygons[not current_polygon])
                current_polygon = not current_polygon


            union.append(current_vertex)
            k = (k + 1) % (len(polygons[current_polygon]))

        union.append(start)
        print('union: ', union)
        return [union]

    def intersection(self):
        if self.no_intersections:
            if check_polygon(self.polygon_b, self.polygon_a[0]):
                return [self.polygon_a]
            if check_polygon(self.polygon_a, self.polygon_b[0]):
                return [self.polygon_b]
            else:
                return []

        intersection = set()
        for p in self.polygon_a[0:-1]:
            if check_polygon(self.polygon_b, p):
                intersection.add(p)
        for q in self.polygon_b[0:-1]:
            if check_polygon(self.polygon_a, q):
                intersection.add(q)
        for s in self.intersections:
            intersection.add(s)

        intersection = list(intersection)
        intersection.append(intersection[0])
        intersection = sort_clockwise(intersection)

        return [intersection]

    def symmetrical_difference(self):
        if self.no_intersections:
            union = self.union()
            overlay = self.intersection()

        overlay_attached = False
        union = self.union()[0]
        overlay = self.intersection()[0][0:-1]
        diff = []
        for k in range(len(union)):
            if union[k] in self.intersections and not overlay_attached:
                entry_point = union[k]
                l = find_index(entry_point, overlay)
                for x in range(len(overlay)):
                    diff.append(overlay[(l+x)%len(overlay)])
                overlay_attached = True
            diff.append(union[k])

        return diff



def resolve_orientation(vertices):
    '''given that the polygon is convex'''
    if len(vertices) < 4:
        return
    vec_a = (vertices[1][0] - vertices[0][0],
             - vertices[1][1] + vertices[0][1])
    vec_b = (vertices[2][0] - vertices[1][0],
             - vertices[2][1] + vertices[1][1])
    orientation = vec_a[0]*vec_b[1] - vec_a[1]*vec_b[0] < 0

    print(['counter-clockwise', 'clockwise'][orientation])
    print([vertices, list(reversed(vertices))][orientation])

    return [vertices, list(reversed(vertices))][orientation]


def beam_intersection(a, b, c):
    """-1 if the beam intersects with the segment
        1 if the beam doesn't intersect with the segment
        0 if the point belongs to the segment"""
    ad = a[0] - c[0], - a[1] + c[1]
    bd = b[0] - c[0], - b[1] + c[1]
    if ad[1] * bd[1] > 0:
        return 1
    sign = lambda x: (x > 0) - (x < 0)
    s = sign(ad[0]*bd[1] - ad[1]*bd[0])

    if s == 0:
        if ad[0]*bd[0] <= 0:
            return 0
        return 1

    if ad[1] < 0:
        return -s
    if bd[1] < 0:
        return s
    return 1


def check_polygon(polygon, point):
    '''returns 1 if the point is inside the polygon, 0 if outside'''
    if polygon[0] != polygon[-1]:
        polygon.append(polygon[0])
    intersection_count = 0
    for k in range(len(polygon) - 1):
        if beam_intersection(polygon[k], polygon[k+1], point) < 0:
            intersection_count += 1

    return intersection_count%2

def intersect_segments(p1, q1, p2, q2):
    a1 = p1[1] - q1[1]
    a2 = p2[1] - q2[1]
    b1 = q1[0] - p1[0]
    b2 = q2[0] - p2[0]
    c1 = - p1[1]*(q1[0] - p1[0]) - p1[0]*(p1[1] - q1[1])
    c2 = - p2[1]*(q2[0] - p2[0]) - p2[0]*(p2[1] - q2[1])

    if a1*b2 - a2*b1 == 0:
        return False

    cross = int((b1*c2 - b2*c1)/(a1*b2 - a2*b1)),\
            int((c1*a2 - c2*a1)/(a1*b2 - a2*b1))

    if min(p1[0], q1[0]) <= cross[0] <= max(p1[0], q1[0]) and\
                            min(p2[0], q2[0]) <= cross[0] < max(p2[0], q2[0]):
        if min(p1[1], q1[1]) <= cross[1] <= max(p1[1], q1[1]) and\
                                min(p2[1], q2[1]) <= cross[1] <= max(p2[1], q2[1]):
            return cross

    else:
        return False


def find_index(item, list):
    for i in range(len(list)):
        if list[i] == item:
            return i


def find_angle(a, c):
    av = (a[0] - c[0], c[1] - a[1])
    return math.atan2(av[1], av[0])


def sort_clockwise(points):
    xc = 0
    yc = 0
    for p in points[0:-1]:
        xc += p[0]/(len(points) - 1)
        yc += p[1]/(len(points) - 1)

    compare = lambda p: find_angle(p, (xc, yc))
    points = sorted(points[0:-1], key=compare)
    points.append(points[0])

    return points


def main():
    app = QtGui.QApplication(sys.argv)
    k = FourthTask()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
