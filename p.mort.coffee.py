import sys
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QTextEdit, QHBoxLayout, QMessageBox
)
from PySide6.QtGui import QFont, QIcon
import subprocess
import pyperclip
import os
import shlex


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("p.mort.coffee")
        self.resize(250, 300)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.upload_button = QPushButton("Upload File")
        self.upload_button.clicked.connect(self.upload_file)
        self.layout.addWidget(self.upload_button)

        self.progress_label = QLabel("Upload Progress:")
        self.layout.addWidget(self.progress_label)

        self.countdown_label = QLabel()
        self.countdown_label.setFont(QFont("Arial", 24))
        self.layout.addWidget(self.countdown_label)

        self.output_text = QTextEdit()
        self.layout.addWidget(self.output_text)

        self.link_button_layout = QHBoxLayout()
        self.layout.addLayout(self.link_button_layout)

        self.link_label = QLabel()
        self.link_label.setFont(QFont("Arial", 12))
        self.link_button_layout.addWidget(self.link_label)

        self.copy_link_button = QPushButton("Copy Link")
        self.copy_link_button.clicked.connect(self.copy_link)
        self.copy_link_button.setEnabled(False)
        self.link_button_layout.addWidget(self.copy_link_button)

        if len(sys.argv) > 1:
            self.file_path_from_arg = sys.argv[1]
            self.timer = QTimer()
            self.timer.timeout.connect(self.upload_file_from_arg)
            self.timer.setSingleShot(True)
            self.timer.start(1000)

    def upload_file_from_arg(self):
        self.handle_upload(self.file_path_from_arg)

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName()
        if file_path:
            self.handle_upload(file_path)

    def handle_upload(self, file_path, insecure=False):
        if not os.path.exists(file_path):
            self.output_text.setText("Error: Invalid file path provided.")
            self.progress_label.setText("Upload Failed!")
            return

        file_size = os.path.getsize(file_path)
        max_size = 100 * 1024 * 1024

        if file_size > max_size:
            self.output_text.setText("Error: File size exceeds the 100 MB limit.")
            self.progress_label.setText("Upload Failed!")
            return

        try:
            quoted_file_path = shlex.quote(file_path)
            curl_command = f"curl {'--insecure' if insecure else ''} --upload-file {quoted_file_path} https://p.mort.coffee"
            output = subprocess.check_output(curl_command, shell=True).decode('utf-8')

            if any(error in output for error in ["413", "Request Entity Too Large"]):
                self.output_text.setText("Error 413: File too large.")
                self.progress_label.setText("Upload Failed!")
            elif any(error in output for error in ["404", "Not Found"]):
                self.output_text.setText("Error 404: URL not found.")
                self.progress_label.setText("Upload Failed!")
            elif any(error in output for error in ["502", "Bad Gateway"]):
                self.output_text.setText("Error 502: Bad Gateway.")
                self.progress_label.setText("Upload Failed!")
            else:
                self.output_text.setText(f"Upload complete. The link is {output.strip()}")
                self.link_label.setText(output.strip())
                self.copy_link_button.setEnabled(True)
                self.progress_label.setText("Upload Complete!")

        except subprocess.CalledProcessError as e:
            if "SSL certificate problem" in str(e):
                user_response = QMessageBox.warning(
                    self,
                    "SSL Certificate Problem",
                    "curl: (60) SSL certificate problem: certificate has expired\nDo you want to continue anyway?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if user_response == QMessageBox.Yes:
                    self.handle_upload(file_path, insecure=True)
                    return
            self.output_text.setText(f"Error: {e}")
            self.progress_label.setText("Upload Failed!")

        self.start_countdown()

    def start_countdown(self):
        self.countdown_seconds = 40
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_timer.start(1000)

    def update_countdown(self):
        if self.countdown_seconds > 0:
            self.countdown_label.setText(str(self.countdown_seconds))
            self.countdown_seconds -= 1
        else:
            self.countdown_timer.stop()
            self.close()

    def copy_link(self):
        link = self.link_label.text()
        pyperclip.copy(link)
        self.copy_link_button.setText("Copied!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        app.setWindowIcon(QIcon("p.mort.coffee.png"))
    except Exception as e:
        print(f"[ERROR] unable to load the window icon : {e}")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
