import os
import smtplib
import ssl
import sys

from datetime import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.content_label_edit = None
        self.button = None
        self.file_button = None
        self.file_label = None
        self.content_label = None
        self.receiver_email_edit = None
        self.receiver_email_label = None
        self.password_edit = None
        self.password_label = None
        self.sender_email_edit = None
        self.sender_email_label = None
        self.file_path = None
        self.init_ui()

    def init_ui(self):
        self.sender_email_label = QLabel('Sender Email ID:', self)
        self.sender_email_label.move(25, 10)
        self.sender_email_edit = QLineEdit(self)
        self.sender_email_edit.move(140, 10)

        self.password_label = QLabel('Password:', self)
        self.password_label.move(25, 40)
        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.move(140, 40)

        self.receiver_email_label = QLabel('Receiver Email ID:', self)
        self.receiver_email_label.move(25, 70)
        self.receiver_email_edit = QLineEdit(self)
        self.receiver_email_edit.move(140, 70)

        self.content_label = QLabel('Content', self)
        self.content_label.move(25, 100)
        self.content_label_edit = QLineEdit(self)
        self.content_label_edit.move(140, 100)

        self.file_label = QLabel(self)
        self.file_label.move(25, 190)
        self.file_label.resize(600, 30)
        self.file_label.setText('No file selected')

        self.file_button = QPushButton('Attach', self)
        self.file_button.move(25, 130)
        self.file_button.clicked.connect(self.open_file_dialog)

        self.button = QPushButton('Send Email', self)
        self.button.move(105, 160)
        self.button.clicked.connect(self._send_email)

        self.button = QPushButton('Remove Attachment', self)
        self.button.move(180, 130)
        self.button.clicked.connect(self._remove_attachment)

        self.setGeometry(100, 100, 350, 250)
        self.setWindowTitle('Send Email')
        self.show()

    def _remove_attachment(self):
        self.file_label.setText('No file selected')
        self.file_path = None

    def open_file_dialog(self):
        # Open a file picker dialog and get the selected file path
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, 'Attach', '', 'All Files (*);;Text Files (*.txt)',
                                                   options=options)
        self.file_path = file_path
        if file_path:
            self.file_label.setText(f"Attached:\n{file_path}")

    def _send_email(self):
        self.file_label.setText("Email sent successfully!")

        email_sender = self.sender_email_edit.text()
        email_password = self.password_edit.text()
        email_receiver = self.receiver_email_edit.text()
        subject = f"Demo Test @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        body = self.content_label_edit.text() if self.content_label_edit.text() else "NO TEXT PROVIDED"

        email_message = MIMEMultipart()
        email_message["From"] = email_sender
        email_message["To"] = email_receiver
        email_message["Subject"] = subject
        email_message.attach(MIMEText(body))

        if self.file_path:
            with open(self.file_path, 'rb') as f:
                image = MIMEImage(f.read())
                image.add_header('Content-Disposition', 'attachment', filename=os.path.basename(self.file_path))
                email_message.attach(image)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            try:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, email_message.as_string())
            except smtplib.SMTPAuthenticationError as err:
                self.file_label.setText(f"Auth error with error code: {err.smtp_code}")
                return
        self.file_label.setText("Email sent successfully!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
