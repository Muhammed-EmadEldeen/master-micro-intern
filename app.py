import sys
import matplotlib
from PySide2.QtWidgets import (
    QLabel, QMainWindow, QMessageBox, QVBoxLayout, QHBoxLayout, QWidget,
    QApplication, QPushButton, QLineEdit, QStackedLayout, QDoubleSpinBox
)
from PySide2.QtGui import QFont
from PySide2.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import expression_processing

matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_ui()
        self.show()

    def init_ui(self):
        self.layout = QStackedLayout()
        self.init_input_screen()
        self.init_plot_screen()

        main_widget = QWidget()
        main_widget.setLayout(self.layout)
        self.setCentralWidget(main_widget)

    def init_input_screen(self):
        equation_label = QLabel("Equation")
        equation_label.setFont(QFont('Arial', 20))
        equation_label.setAlignment(Qt.AlignCenter)
        self.equation_field = QLineEdit()
        self.min_value = self.create_spinbox()
        self.max_value = self.create_spinbox()

        min_max_layout = QHBoxLayout()

        min_box = QVBoxLayout()
        spinbox_label = QLabel('Minimum X Value')
        min_box.addWidget(spinbox_label)
        min_box.addWidget(self.min_value)
        min_widget = QWidget()
        min_widget.setLayout(min_box)

        max_box = QVBoxLayout()
        spinbox_label = QLabel('Maximum X Value')
        max_box.addWidget(spinbox_label)
        max_box.addWidget(self.max_value)
        max_widget = QWidget()
        max_widget.setLayout(max_box)

        min_max_layout.addWidget(min_widget)
        min_max_layout.addWidget(max_widget)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.create_button('Clear', self.clear))
        buttons_layout.addWidget(self.create_button('Submit', self.submit))

        input_layout = QVBoxLayout()
        input_layout.addWidget(equation_label)
        input_layout.addWidget(self.equation_field)
        input_layout.addSpacing(200)
        input_layout.addLayout(min_max_layout)
        input_layout.addSpacing(200)
        input_layout.addLayout(buttons_layout)

        input_widget = QWidget()
        input_widget.setLayout(input_layout)
        self.layout.addWidget(input_widget)

    def init_plot_screen(self):
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        toolbar = NavigationToolbar(self.sc, self)
        back_button = self.create_button('Back', self.back_screen)

        plot_layout = QVBoxLayout()
        plot_layout.addWidget(toolbar)
        plot_layout.addWidget(self.sc)
        plot_layout.addWidget(back_button)

        plot_widget = QWidget()
        plot_widget.setLayout(plot_layout)
        self.layout.addWidget(plot_widget)

    def create_spinbox(self):
        spinbox = QDoubleSpinBox(minimum=-1000, maximum=1000)
        return spinbox

    def create_button(self, text, callback):
        button = QPushButton(text, self)
        button.clicked.connect(callback)
        return button

    def back_screen(self):
        self.layout.setCurrentIndex(0)

    def submit(self):
        equation_is_valid, message = expression_processing.inspect_equation(
            self.equation_field.text())
        if equation_is_valid:
            self.plot_equation()
        else:
            self.show_error("Wrong Input", message)

    def plot_equation(self):
        try:
            x_values = expression_processing.get_x_values(
                self.min_value.value(), self.max_value.value())
            y_values = [expression_processing.evaluate_expression_sympy(
                self.equation_field.text(), x) for x in x_values]
            self.update_plot(x_values, y_values)
            self.layout.setCurrentIndex(1)
        except Exception as e:
            self.show_error("Plotting Error", str(e))

    def update_plot(self, x, y):
        self.sc.axes.clear()
        self.sc.axes.plot(x, y)
        self.sc.draw()

    def show_error(self, title, message):
        QMessageBox.critical(self, title, message, buttons=QMessageBox.Ok)
        print(message)

    def clear(self):
        self.equation_field.clear()
        self.min_value.setValue(0)
        self.max_value.setValue(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
