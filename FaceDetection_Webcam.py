import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage

class Model:
    def __init__(self):
        self.video_capture = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.detect_faces)

    def start_webcam(self):
        self.video_capture = cv2.VideoCapture(0)  # 0 corresponds to the default webcam
        self.timer.start(100)  # Set the timer to trigger every 100 ms (adjust as needed)

    def stop_webcam(self):
        if self.video_capture is not None:
            self.video_capture.release()
            self.timer.stop()

    def detect_faces(self):
        if self.video_capture is not None:
            ret, frame = self.video_capture.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3)
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                view.display_frame(frame)

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

        self.detect_button = QPushButton("Start Webcam")
        self.layout.addWidget(self.detect_button)
        self.detect_button.clicked.connect(self.toggle_webcam)

    def display_frame(self, frame):
        if frame is not None:
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap)
            self.image_label.setAlignment(Qt.AlignCenter)

    def toggle_webcam(self):
        if model.video_capture is None:
            model.start_webcam()
            self.detect_button.setText("Stop Webcam")
        else:
            model.stop_webcam()
            self.detect_button.setText("Start Webcam")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = Model()
    view = View()
    model.detect_faces()  # Start face detection immediately
    view.show()
    sys.exit(app.exec_())
