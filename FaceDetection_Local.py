import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage

class Model:
    def __init__(self):
        self.image = None

    def load_image(self, image_path):
        self.image = cv2.imread(image_path)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        return self.image

    def detect_faces(self):
        if self.image is not None:
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
            for (x, y, w, h) in faces:
                cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            return self.image

class View(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face Detection App")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.image_label = QLabel()
        self.layout.addWidget(self.image_label)

        self.load_button = QPushButton("Load Image")
        self.detect_button = QPushButton("Detect Faces")
        self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.detect_button)
        self.load_button.clicked.connect(self.load_image)
        self.detect_button.clicked.connect(self.detect_faces)

    def display_image(self, image):
        if image is not None:
            height, width, channel = image.shape
            bytes_per_line = 3 * width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)
            self.image_label.setAlignment(Qt.AlignCenter)
            self.image_label.resize(600,400)

    def load_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.jpg *.png *.bmp);;All Files (*)", options=options)
        if file_path:
            controller.load_image(file_path)

    def detect_faces(self):
        image_with_faces = controller.detect_faces()
        self.display_image(image_with_faces)

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def load_image(self, image_path):
        image = self.model.load_image(image_path)
        self.view.display_image(image)

    def detect_faces(self):
        return self.model.detect_faces()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = Model()
    view = View()
    controller = Controller(model, view)
    view.show()
    sys.exit(app.exec_())
