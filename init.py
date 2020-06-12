import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog, QComboBox, QLineEdit
from PyQt5 import uic
import constants
import app as crawler

# https://wikidocs.net/35477

# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType(os.getcwd()+"/app.ui")[0]

# 화면을 띄우는데 사용되는 Class 선언


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.coupang_pw_edit.setEchoMode(QLineEdit.Password)
        self.dir_edit.setText(os.getcwd())
        self.categories.addItems(
            [category["name"] for category in constants.COUPANG_SEARCH_CATEGORIES])

        # 버튼에 기능을 연결하는 코드
        self.start.clicked.connect(self.clicked_start)
        self.set_dir.clicked.connect(self.clicked_set_dir)

    # start버튼이 눌리면 작동할 함수
    def clicked_start(self):
        if self.validate_input():
            crawler.start()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('입력을 다시 확인하세요')
            msg.setWindowTitle("Error")
            msg.exec_()

    def clicked_set_dir(self):
        try:
            path = QFileDialog.getExistingDirectory(
                self, 'Open Directory', os.getcwd(), QFileDialog.ShowDirsOnly)
            self.dir_edit.setText(path)
        except Exception as e:
            raise Exception(e)

    def validate_input(self):
        try:
            id = self.coupang_id_edit.text()
            pw = self.coupang_pw_edit.text()
            word = self.search_word_edit.text()
            count = self.search_count_edit.text()
            path = self.dir_edit.text()

            if (id and pw and word and int(count) and path):
                constants.COUPANG_ID = id
                constants.COUPANG_PW = pw
                constants.COUPANG_SEARCH_WORD = word
                constants.COUPANG_SEARCH_COUNT = int(count)
                constants.COUPANG_RESULT_DIR = path
                constants.COUPANG_SEARCH_CATEGORYID = list(filter(
                    lambda x: x['name'] == self.categories.currentText(), constants.COUPANG_SEARCH_CATEGORIES))[0]['id']
                return True
            else:
                return False
        except Exception as e:
            print('validate_input Error : ', e)
            return False


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)
    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
