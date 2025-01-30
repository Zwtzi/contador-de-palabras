import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog
from PyQt6.QtGui import QPixmap, QImage

class WordCounterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Contador de Palabras')
        self.setGeometry(100, 100, 800, 600)

        self.image_label = QLabel(self)
        self.image_label.setScaledContents(True)

        self.button = QPushButton('Seleccionar Imagen', self)
        self.button.clicked.connect(self.loadImage)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def loadImage(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Seleccionar Imagen', '', 'Images (*.png *.jpg *.jpeg)')
        if file_name:
            word_count, processed_image = self.countWords(file_name)
            print(f'Palabras detectadas: {word_count}')
            self.displayImage(processed_image)

    def countWords(self, image_path):
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 10))
        dilated = cv2.dilate(thresh, kernel, iterations=1)
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        word_count = 0
        min_area = 100
        max_area = 10000

        for contour in contours:
            area = cv2.contourArea(contour)
            if min_area < area < max_area:
                word_count += 1
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return word_count, image

    def displayImage(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        bytes_per_line = channel * width
        q_img = QImage(image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        self.image_label.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WordCounterApp()
    window.show()
    sys.exit(app.exec())
