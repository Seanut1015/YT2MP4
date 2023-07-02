from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets
from pytube import YouTube
from PyQt5.QtCore import Qt
from UI import Ui_Form
from requests import get
import time
import sys
from os import path


class MyWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.def_download = path.join(path.expanduser("~"), "Desktop")
        self.label_2.setText(self.def_download)

    def open_file(self):
        Path = QtWidgets.QFileDialog.getExistingDirectory()
        Path = "".join(Path)
        self.label_2.setText(Path)

    def onProgress(self, stream, chunk, remains):
        total = stream.filesize
        per = int((total - remains) / total * 100)
        self.progressBar.setValue(per)
        if per == 100:
            self.done()

    def url_in(self):
        url = self.lineEdit.text()
        if url != "":
            yt = YouTube(url, on_progress_callback=self.onProgress)
            self.yt = yt
            title = yt.title
            self.lineEdit_1.setText(title)
            req = get(yt.thumbnail_url)  # requests
            photo = QPixmap()
            photo.loadFromData(req.content)
            self.label_3.setPixmap(
                photo.scaled(self.label_3.size(), aspectRatioMode=Qt.KeepAspectRatio)
            )
            self.lineEdit.setReadOnly(1)

    def re(self):
        self.lineEdit.clear()
        self.lineEdit_1.clear()
        self.label_3.clear()
        self.progressBar.setValue(0)
        self.pushButton_1.setText("下載")
        self.lineEdit.setReadOnly(0)

    def download(self):
        if self.pushButton_1.text() == "下載":
            self.progressBar.setValue(1)
            name = self.lineEdit_1.text()  # encoding="utf-8-sig"
            try:
                self.yt.streams.filter().get_highest_resolution().download(
                    self.label_2.text(), filename=name + ".mp4"
                )
            except:
                for i in range(0, 102, 2):
                    self.progressBar.setValue(i)
                    time.sleep(0.01)
                self.pushButton_1.setText("錯誤")
        else:
            self.re()

    def done(self):
        self.pushButton_1.setText("完成")


app = QtWidgets.QApplication(sys.argv)
ui = MyWindow()
ui.setWindowTitle("YT2MP4")
ui.show()
sys.exit(app.exec_())
