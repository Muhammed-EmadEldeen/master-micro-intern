import pytest
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt
# Assuming your main window file is named main_window.py
from app import MainWindow
from PySide2.QtWidgets import (
    QLabel, QMainWindow, QMessageBox, QVBoxLayout, QHBoxLayout, QWidget,
    QApplication, QPushButton, QLineEdit, QStackedLayout, QDoubleSpinBox
)


@pytest.fixture
def app(qtbot):
    if QApplication.instance() is None:
        QApplication([])  # Create a QApplication instance if none exists
    window = MainWindow()
    qtbot.addWidget(window)
    return window


def test_initial_state(app):
    assert app.layout.currentIndex() == 0
    assert app.equation_field.text() == ''
    assert app.min_value.value() == 0
    assert app.max_value.value() == 0


def test_submit_valid_equation(qtbot, app):
    qtbot.keyClicks(app.equation_field, 'x + 2')
    app.min_value.setValue(0)
    app.max_value.setValue(10)
    qtbot.mouseClick(app.layout.currentWidget().findChild(
        QPushButton, 'Submit'), Qt.LeftButton)

    assert app.layout.currentIndex() == 1


def test_submit_invalid_equation(qtbot, app):
    qtbot.keyClicks(app.equation_field, 'x ++ 2')
    qtbot.mouseClick(app.layout.currentWidget().findChild(
        QPushButton, 'Submit'), Qt.LeftButton)

    assert app.layout.currentIndex() == 0


def test_clear_button(qtbot, app):
    qtbot.keyClicks(app.equation_field, 'x + 2')
    app.min_value.setValue(5)
    app.max_value.setValue(15)
    qtbot.mouseClick(app.layout.currentWidget().findChild(
        QPushButton, 'Clear'), Qt.LeftButton)

    assert app.equation_field.text() == ''
    assert app.min_value.value() == 0
    assert app.max_value.value() == 0


def test_back_button(qtbot, app):
    qtbot.keyClicks(app.equation_field, 'x + 2')
    app.min_value.setValue(0)
    app.max_value.setValue(10)
    qtbot.mouseClick(app.layout.currentWidget().findChild(
        QPushButton, 'Submit'), Qt.LeftButton)

    qtbot.mouseClick(app.layout.currentWidget().findChild(
        QPushButton, 'Back'), Qt.LeftButton)
    assert app.layout.currentIndex() == 0
