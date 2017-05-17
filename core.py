from PyQt4 import QtCore, QtGui
import one, two, three, four, five
import sys
import math


W_HEIGHT = 480
W_WIDTH = 720

class AppCore(QtGui.QTabWidget):

    def __init__(self):
        super(AppCore, self).__init__()
        self.tab1 = QtGui.QWidget()
        self.tab1_content = one.FirstTask(-3, 0.2, 1, 1)
        self.tab2 = QtGui.QWidget()
        self.tab2_content = two.SecondTask(0, 2, 2)
        self.tab3 = QtGui.QWidget()
        self.tab3_content = three.ThirdTask(1, 1, 3, 3)
        self.tab4 = QtGui.QWidget()
        self.tab4_content = four.FourthTask()
        self.tab5 = QtGui.QWidget()
        self.tab5_content = five.FifthTask(-5, 5, -5, 5)
        self.tab6 = QtGui.QWidget()

        self.setGeometry(50, 50, W_WIDTH, W_HEIGHT)
        self.setFixedSize(W_WIDTH, W_HEIGHT)
        self.setWindowTitle("KGG")

        self.addTab(self.tab1, "First task")
        self.addTab(self.tab2, "Second task")
        self.addTab(self.tab3, "Third task")
        self.addTab(self.tab4, "Fourth task")
        self.addTab(self.tab5, "Fifth task")
        self.addTab(self.tab6, "Sixth task")

        self.init_tab1()
        self.init_tab2()
        self.init_tab3()
        self.init_tab4()
        self.init_tab5()

    def init_tab1(self):
        g_layout = QtGui.QGridLayout()
        g_layout.setSpacing(5)
        g_layout.setColumnStretch(1, 1)
        g_layout.addWidget(self.tab1_content, 0, 0)

        a_label = QtGui.QLabel("Parameter a: ")
        a_label.setMaximumHeight(20)
        a_label.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        a_field = QtGui.QLineEdit()
        a_field.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        g_layout.addWidget(a_label, 1, 1)
        g_layout.addWidget(a_field, 1, 2)

        b_label = QtGui.QLabel("Parameter b: ")
        b_label.setMaximumHeight(20)
        b_label.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        b_field = QtGui.QLineEdit()
        b_field.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        g_layout.addWidget(b_label, 1, 3)
        g_layout.addWidget(b_field, 1, 4)

        s_label = QtGui.QLabel("Start: ")
        s_label.setMaximumHeight(20)
        s_label.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        s_field = QtGui.QLineEdit()
        s_field.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        g_layout.addWidget(s_label, 1, 5)
        g_layout.addWidget(s_field, 1, 6)

        e_label = QtGui.QLabel("End: ")
        e_label.setMaximumHeight(20)
        e_label.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        e_field = QtGui.QLineEdit()
        e_field.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        g_layout.addWidget(e_label, 1, 7)
        g_layout.addWidget(e_field, 1, 8)

        def button_handler():
            all_is_cool = validate_input(e_field.text()) and\
                          validate_input(s_field.text()) and\
                          validate_input(a_field.text()) and\
                          validate_input(b_field.text())

            if all_is_cool and s_field.text() != e_field.text():
                self.tab1_content.adjust(float(s_field.text()),
                                         float(e_field.text()),
                                         float(a_field.text()),
                                         float(b_field.text()))
                self.tab1_content.update()

        draw_button = QtGui.QPushButton("Draw")
        draw_button.clicked.connect(button_handler)
        g_layout.addWidget(draw_button, 1, 9)

        self.tab1.setLayout(g_layout)

    def init_tab2(self):
        g_layout = QtGui.QGridLayout()
        g_layout.setSpacing(5)
        g_layout.setColumnStretch(1, 1)
        g_layout.addWidget(self.tab2_content, 0, 0)

        a_label = QtGui.QLabel("Parameter a: ")
        a_label.setMaximumHeight(20)
        a_label.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        a_field = QtGui.QLineEdit()
        a_field.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        g_layout.addWidget(a_label, 1, 1)
        g_layout.addWidget(a_field, 1, 2)

        s_label = QtGui.QLabel("Start: pi* ")
        s_label.setMaximumHeight(20)
        s_label.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        s_field = QtGui.QLineEdit()
        s_field.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        g_layout.addWidget(s_label, 1, 3)
        g_layout.addWidget(s_field, 1, 4)

        e_label = QtGui.QLabel("End: pi*")
        e_label.setMaximumHeight(20)
        e_label.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        e_field = QtGui.QLineEdit()
        e_field.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        g_layout.addWidget(e_label, 1, 5)
        g_layout.addWidget(e_field, 1, 6)

        def button_handler():
            all_is_cool = validate_input(e_field.text()) and \
                          validate_input(s_field.text()) and \
                          validate_input(a_field.text())

            if all_is_cool and s_field.text() != e_field.text():
                self.tab2_content.adjust(float(s_field.text()),
                                         float(e_field.text()),
                                         float(a_field.text()))
                self.tab2_content.update()

        draw_button = QtGui.QPushButton("Draw")
        draw_button.clicked.connect(button_handler)
        g_layout.addWidget(draw_button, 1, 7)

        self.tab2.setLayout(g_layout)

    def init_tab3(self):
        g_layout = QtGui.QGridLayout()
        g_layout.setSpacing(5)
        g_layout.setColumnStretch(1, 1)
        g_layout.addWidget(self.tab3_content, 0, 0)

        a_label = QtGui.QLabel("Parameter a: ")
        a_label.setMaximumHeight(20)
        a_label.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        a_field = QtGui.QLineEdit()
        a_field.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        g_layout.addWidget(a_label, 1, 1)
        g_layout.addWidget(a_field, 1, 2)


        x_label = QtGui.QLabel("x interval: ")
        x_label.setMaximumHeight(20)
        x_label.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        x_field = QtGui.QLineEdit()
        x_field.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        g_layout.addWidget(x_label, 1, 3)
        g_layout.addWidget(x_field, 1, 4)

        y_label = QtGui.QLabel("y interval: ")
        y_label.setMaximumHeight(20)
        y_label.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        y_field = QtGui.QLineEdit()
        y_field.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        g_layout.addWidget(y_label, 1, 5)
        g_layout.addWidget(y_field, 1, 6)

        def button_handler():
            all_is_cool = validate_input(a_field.text()) and \
                          validate_input(x_field.text()) and \
                          validate_input(y_field.text())

            if all_is_cool and float(x_field.text()) > 0 and float(y_field.text()) > 0:
                self.tab3_content.adjust(float(a_field.text()),
                                         float(x_field.text()),
                                         float(y_field.text()))
                self.tab3_content.update()

        draw_button = QtGui.QPushButton("Draw")
        draw_button.clicked.connect(button_handler)
        g_layout.addWidget(draw_button, 1, 7)

        self.tab3.setLayout(g_layout)

    def init_tab4(self):
        g_layout = QtGui.QGridLayout()
        g_layout.setSpacing(5)
        g_layout.setColumnStretch(1, 1)
        g_layout.addWidget(self.tab4_content, 0, 0)

        def clear_button_handler():
            self.tab4_content.clear()
            self.tab4_content.update()

        clear_button = QtGui.QPushButton("Clear")
        clear_button.clicked.connect(clear_button_handler)
        g_layout.addWidget(clear_button, 1, 1)

        def clip_button_handler():
            self.tab4_content.clip()
            self.tab4_content.update()

        clip_button = QtGui.QPushButton("Clip")
        clip_button.clicked.connect(clip_button_handler)
        g_layout.addWidget(clip_button, 1, 2)

        self.tab4.setLayout(g_layout)

    def init_tab5(self):
        g_layout = QtGui.QGridLayout()
        g_layout.setSpacing(5)
        g_layout.setColumnStretch(1, 1)

        g_layout.addWidget(self.tab5_content, 0, 0)

        a_label = QtGui.QLabel("x from: ")
        a_label.setMaximumHeight(20)
        a_label.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        a_field = QtGui.QLineEdit()
        a_field.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        g_layout.addWidget(a_label, 1, 1)
        g_layout.addWidget(a_field, 1, 2)

        b_label = QtGui.QLabel("x to: ")
        b_label.setMaximumHeight(20)
        b_label.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        b_field = QtGui.QLineEdit()
        b_field.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        g_layout.addWidget(b_label, 1, 3)
        g_layout.addWidget(b_field, 1, 4)

        s_label = QtGui.QLabel("y from: ")
        s_label.setMaximumHeight(20)
        s_label.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        s_field = QtGui.QLineEdit()
        s_field.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        g_layout.addWidget(s_label, 1, 5)
        g_layout.addWidget(s_field, 1, 6)

        e_label = QtGui.QLabel("y to: ")
        e_label.setMaximumHeight(20)
        e_label.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        e_field = QtGui.QLineEdit()
        e_field.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        g_layout.addWidget(e_label, 1, 7)
        g_layout.addWidget(e_field, 1, 8)

        def button_handler():
            all_is_cool = validate_input(e_field.text()) and\
                          validate_input(s_field.text()) and\
                          validate_input(a_field.text()) and\
                          validate_input(b_field.text())

            if all_is_cool and s_field.text() != e_field.text():
                self.tab5_content.adjust(float(s_field.text()),
                                         float(e_field.text()),
                                         float(a_field.text()),
                                         float(b_field.text()))
                self.tab5_content.draw()
                self.tab5_content.update()

        draw_button = QtGui.QPushButton("Draw")
        draw_button.clicked.connect(button_handler)
        g_layout.addWidget(draw_button, 1, 9)

        self.tab5.setLayout(g_layout)


def validate_input(text):
    try:
        float(text)
        return True
    except ValueError:
        return False


def main():
    app = QtGui.QApplication(sys.argv)
    main_window = AppCore()
    main_window.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
