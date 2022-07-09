'''
Author: scikkk 203536673@qq.com
Date: 2022-07-07 21:55:15
LastEditors: scikkk
LastEditTime: 2022-07-10 01:43:59
Description: program entry
'''

import sys
from interface.ime import IMeMainWindow
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IMeMainWindow()
    window.show()
    sys.exit(app.exec_())
