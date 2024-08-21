import os
import sys
import time

from PySide6.QtCore import QUrl, Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QWidget
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtGui import QCursor


os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--no-sandbox --enable-logging --log-level=0"


class Widgets(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setCursor(Qt.BlankCursor)
        self.widget = QWidget(self)

        self.browser = QWebEngineView()
        self.browser.load(QUrl("http://patrik-face"))
        self.setCentralWidget(self.browser)


if __name__ == "__main__":
    time.sleep(1)

    app = QApplication(sys.argv)
    # QCursor.setPos(0, 0)
    window = Widgets()
    window.showFullScreen()
    sys.exit(app.exec())
