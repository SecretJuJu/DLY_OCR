from PyQt5.QtCore import Qt

from ocr import ocr
#ocr(image_path)
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog, QLabel, QDialog


class MyApp(QWidget):

    file_path = ""
    filename_label = None


    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        ok_button = QPushButton('OK')
        file_button = QPushButton('select')
        file_button.clicked.connect(self.showFileDialog)	# 클릭 시 실행할 function
        ok_button.clicked.connect(self.callOcr)

        h_filename_box = QHBoxLayout()

        self.filename_label = QLabel('')
        self.filename_label.setAlignment(Qt.AlignCenter)

        h_filename_box.addStretch(1)
        h_filename_box.addWidget(self.filename_label)
        h_filename_box.addStretch(1)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(file_button)
        hbox.addWidget(ok_button)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(h_filename_box)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)

        self.setWindowTitle('DLY_OCR')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def showFileDialog(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file', './')

            if fname[0]:
                print(fname)
                self.file_path = fname[0]
                self.filename_label.setText(fname[0])
        except Exception as e:
            print("err")

    def callOcr(self):
        if(self.file_path):
            print(self.file_path)
            data = ocr(image_path=self.file_path)
            with open(self.file_path+"_result.txt","w") as f:
                f.write(data)
        else :
            print("no selected")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MyApp()
    sys.exit(app.exec_())
