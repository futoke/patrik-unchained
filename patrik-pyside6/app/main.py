import sys

from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView


class Widgets(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.widget = QWidget(self)

        self.browser = QWebEngineView()
        self.browser.load(QUrl("http://patrik-face"))
        self.setCentralWidget(self.browser)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Widgets()
    window.showFullScreen()
    sys.exit(app.exec())
