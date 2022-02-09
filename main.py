import os
import sys

import requests
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox
from PyQt5.Qt import Qt

SCREEN_SIZE = [600, 450]
SCALE = input().split()


class Field(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Координаты карты')
        font = QFont(None, 16)
        self.lbl = QLabel(self)
        self.lbl.move(200, 20)
        self.lbl.resize(250, 20)
        self.lbl.setFont(font)
        self.lbl.setText('Введите координаты:')
        self.field1 = QLineEdit(self)
        self.field1.resize(150, 50)
        self.field1.move(225, 100)
        self.field1.setFont(font)
        self.field2 = QLineEdit(self)
        self.field2.resize(150, 50)
        self.field2.move(225, 200)
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
        self.initUI()
        self.getImage()

    def getImage(self):
        PARAMS = {'ll': ','.join(COORDS),
                  'spn': ','.join(map(str, SCALE)),
                  'l': self.sl[self.change_box.currentText()]}
        self.setFocus()
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
        self.showImage()

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.setFocus()
        font = QFont(None, 16)
        self.image = QLabel(self)
        self.image.move(0, 60)
        self.image.resize(600, 390)
        self.change_box = QComboBox(self)
        self.change_box.move(150, 15)
        self.change_box.resize(290, 30)
        self.change_box.addItems(['Карта', 'Спутник', 'Гибрид'])
        self.change_box.setCurrentIndex(0)
        self.change_box.setFont(font)
        self.sl = {'Карта': 'map', 'Спутник': 'sat', 'Гибрид': 'sat,skl'}
        self.change_box.currentTextChanged.connect(self.getImage)

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
            SCALE = [max(float(SCALE[0]) * 0.5, 0.0005), max(float(SCALE[1]) * 0.5, 0.0005)]
            print(SCALE)
        if event.key() == Qt.Key_PageDown:
            SCALE = [min(float(SCALE[0]) * 2, 0.0035), min(float(SCALE[1]) * 2, 0.0035)]
            print(SCALE)
        self.getImage()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Field()
    ex.show()
    sys.exit(app.exec())
