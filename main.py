import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton

SCREEN_SIZE = [600, 450]
SCALE = input().split()


class Field(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 450, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.lbl = QLabel(self)
        self.lbl.move(250, 20)
        self.lbl.resize(150, 20)
        self.lbl.setText('Введите координаты:')
        self.field1 = QLineEdit(self)
        self.field1.resize(100, 50)
        self.field1.move(250, 100)
        self.field2 = QLineEdit(self)
        self.field2.resize(100, 50)
        self.field2.move(250, 200)
        self.btn = QPushButton('Далее', self)
        self.btn.resize(100, 50)
        self.btn.move(250, 300)
        self.btn.clicked.connect(self.run)

    def run(self):
        x = self.field1.text()
        y = self.field2.text()
        global COORDS
        COORDS = [x, y]
        e = Example()
        e.show()
        self.close()





class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()

    def getImage(self):
        PARAMS = {'ll': ','.join(COORDS),
                  'spn': ','.join(SCALE),
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

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)
        self.image.setScaledContents(True)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Field()
    ex.show()
    sys.exit(app.exec())
