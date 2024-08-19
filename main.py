import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from detect_camera_faces import detect_face
from recognize_face import recognize_face
import traceback


class CameraWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 创建一个布局
        self.layout = QVBoxLayout()

        # 创建一个用于显示摄像头画面的 QLabel
        self.label = QLabel()
        self.layout.addWidget(self.label)

        # 创建一个用于关闭摄像头的按钮
        self.close_button = QPushButton('关闭摄像头')
        self.close_button.clicked.connect(self.close_camera)
        self.layout.addWidget(self.close_button)

        self.save_face_button = QPushButton("保存人脸")
        self.save_face_button.clicked.connect(self.save_face)
        self.layout.addWidget(self.save_face_button)

        # 设置布局
        self.setLayout(self.layout)

        # 初始化摄像头
        self.cap = cv2.VideoCapture(0)

        # 创建一个定时器来更新摄像头画面
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # 30ms 刷新一次
        self.detect_result = None
        self.frame = None

    def get_face(self):
        if self.detect_result.size != 0:
            face = self.detect_result.data[0].pos
            x, y, width, height = face.x, face.y, face.width, face.height
            roi = self.frame[y:y+height, x:x+width]
            scale_factor = 2  # 缩放倍数，例如放大2倍
            roi_resized = cv2.resize(roi, (0, 0), fx=scale_factor, fy=scale_factor)
            return roi_resized

    def save_face(self):
        roi_resized = self.get_face()
        cv2.imwrite("test.jpg", roi_resized)

    @property
    def display_frame(self):
        frame = self.frame.copy()
        for i in range(self.detect_result.size):
            face = self.detect_result.data[i].pos
            cv2.rectangle(frame, (face.x, face.y), (face.x + face.width, face.y + face.height), (255, 0, 0), 2)
        return frame

    def update_frame(self):
        # 读取摄像头画面
        try:
            ret, self.frame = self.cap.read()
            self.detect_result = detect_face(self.frame)
            face_in_frame = self.get_face()
            if face_in_frame is not None:
                target_face = cv2.imread("target.jpg")
                similiar = recognize_face(face_in_frame, target_face)
                print(similiar)
            if ret:
                # 将 BGR 格式转换为 RGB 格式
                rgb_image = cv2.cvtColor(self.display_frame, cv2.COLOR_BGR2RGB)

                # 将图像转换为 QImage
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

                # 将 QImage 转换为 QPixmap 并显示在 QLabel 中
                self.label.setPixmap(QPixmap.fromImage(qt_image))
        except Exception as e:
            print(e)
            traceback.print_exc()

    def close_camera(self):
        # 释放摄像头并关闭窗口
        self.cap.release()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CameraWidget()
    window.show()
    sys.exit(app.exec_())