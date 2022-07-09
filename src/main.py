'''
Description: 
Author: SciK
Date: 2022-07-07 21:55:15
LastEditors: SciK
LastEditTime: 2022-07-09 22:31:04
FilePath: \mypinyin\src\main.py
'''
import sys
from interface.ime import IMeMainWindow
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = IMeMainWindow()
    window.show()
    sys.exit(app.exec_())
