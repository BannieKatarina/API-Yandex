import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.Qt import Qt

SCREEN_SIZE = [600, 450]

COORDS = input().split()
SCALE = input().split()



class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()

    def getImage(self):
        PARAMS = {'ll': ','.join(COORDS),
                  'spn': ','.join(map(str, SCALE)),
                  'l': 'map'}
        map_request = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_request, params=PARAMS)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.showImage()

    def showImage(self):
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)
        self.image.setScaledContents(True)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        global SCALE
        if event.key() == Qt.Key_PageUp:
            SCALE = [max(float(SCALE[0]) * 0.5, 0.000125), max(float(SCALE[1]) * 0.5, 0.000125)]
            print(SCALE)
        if event.key() == Qt.Key_PageDown:
            SCALE = [min(float(SCALE[0]) * 2, 0.035), min(float(SCALE[1]) * 2, 0.035)]
            print(SCALE)
        self.getImage()
        self.showImage()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
