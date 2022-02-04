import os
import sys

import requests
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.Qt import Qt

SCREEN_SIZE = [600, 450]
SCALE = input().split()


class Field(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        font = QFont(None, 16)
        self.lbl = QLabel(self)
        self.lbl.move(200, 20)
        self.lbl.resize(250, 20)
        self.lbl.setFont(font)
        self.lbl.setText('Введите координаты:')
        self.field1 = QLineEdit(self)
        self.field1.resize(100, 50)
        self.field1.move(250, 100)
        self.field1.setFont(font)
        self.field2 = QLineEdit(self)
        self.field2.resize(100, 50)
        self.field2.move(250, 200)
        self.field2.setFont(font)
        self.btn = QPushButton('Далее', self)
        self.btn.resize(100, 50)
        self.btn.move(250, 300)
        self.btn.setFont(font)
        self.btn.clicked.connect(self.run)

    def run(self):
        x = self.field1.text()
        y = self.field2.text()
        global COORDS
        COORDS = [x, y]
        self.second_form = Example()
        self.second_form.show()
        self.close()


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
    ex = Field()
    ex.show()
    sys.exit(app.exec())
