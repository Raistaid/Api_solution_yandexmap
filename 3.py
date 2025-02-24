import io, os
import sys
import requests
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QButtonGroup, QLabel
from PyQt6.QtCore import Qt



class Map(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ll = '-74.044713, 40.689793'
        self.api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        self.spn = '0.006389, 0.002645'
        self.getImage()
        self.initUI()

    def getImage(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        params = {
            "ll": ",".join(self.ll),
            "spn": ",".join(self.spn),
            "apikey": self.api_key,
        }

        response = requests.get(server_address, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(server_address)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)


    def initUI(self):
        self.setGeometry(100, 100, 700, 700)
        self.setWindowTitle('Отображение карты')
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(100, 100)
        self.image.resize(500, 500)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            self.ll[0] += 1.0
        elif event.key() == Qt.Key.Key_Down:
            self.ll[0] -= 1.0
        elif event.key() == Qt.Key.Key_Left:
            self.ll[1] -= 1.0
        elif event.key() == Qt.Key.Key_Right:
            self.ll[1] += 1.0

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Map()
    ex.show()
    sys.exit(app.exec())