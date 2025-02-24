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
        self.delta = 12

        self.getImage()
        self.initUI()


    def getImage(self):
        # Готовим запрос.
        map_api_server = "https://static-maps.yandex.ru/v1"
        toponym_longitude = "37.677751"
        toponym_lattitude = "55.757718"

        apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

        # Собираем параметры для запроса к StaticMapsAPI:
        map_params = {
            "ll": ",".join([toponym_longitude, toponym_lattitude]),
            "z": self.delta,
            "apikey": apikey,
        }

        response = requests.get(map_api_server, params=map_params)

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        self.pixmap = QPixmap(self.map_file)


    def initUI(self):
        self.setGeometry(100, 100, 700, 700)
        self.setWindowTitle('Отображение карты')
        self.image = QLabel(self)
        self.image.move(100, 100)
        self.image.resize(500, 500)
        self.image.setPixmap(self.pixmap)

    def update_map(self):
        self.getImage()
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp:
            self.delta += 1
            self.update_map()
        if event.key() == Qt.Key.Key_PageDown:
            self.delta -= 1
            self.update_map()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Map()
    ex.show()
    sys.exit(app.exec())

