'''
Author: scikkk 203536673@qq.com
Date: 2022-07-07 21:37:04
LastEditors: scikkk
LastEditTime: 2022-07-10 01:45:30
Description: IMeMainWindow class
'''

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from hmm.hmm import HMM
from split.pycut import pysplit
from interface.imeui import Ui_mainWindow
from PyQt5.QtGui import QTextCursor


class IMeMainWindow(QMainWindow):
    """
    The main window of input method.

    :param hmm: Hidden Markov Model
    :param ui: Ui_mainWindow
    :param candidate: the candidate Chinese character sequence, e.g., [('描', ...), ('淼', ...), ('緲',), ('米奥', '秘奥', '密奥'), ('米安欧', ...)]
    :param pinyin_lists: the list Pinyin list after split, e.g., [('miao',), ('miao',), ('miao',), ('mi', 'ao'), ('mi', 'a', 'o')]
    :param left_pinyin_lists: the list of Pinyin list splited but not translated
    :param page_num: the page number of the candidate page displayed on the current screen
    """

    def __init__(self, par=None):
        super(IMeMainWindow, self).__init__(parent=par)
        self.hmm = HMM()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.candidate = []
        self.pinyin_lists = []
        self.left_pinyin_lists = []
        self.page_num = 0

    def reset(self) -> None:
        """ Reset some variables."""
        self.page_num = 0
        self.candidate = []
        self.pinyin_lists = []
        self.left_pinyin_lists = []

    def process(self) -> None:
        """ This is the main program of input method. """
        pinyin = self.ui.lineEdit.text().replace("\'", '')
        if 0 < len(pinyin) < 52:
            pinyin_lists = pysplit(pinyin)
            if pinyin_lists:
                # do some reset
                self.reset()
                # translate
                for pinyin_list in pinyin_lists[::-1]:
                    temp, left_pinyin_list = self.hmm.trans(pinyin_list)
                    self.candidate += [temp[i:i + 10]
                                       for i in range(0, len(temp), 10)]
                    self.pinyin_lists += [
                        pinyin_list for _ in range(0, len(temp), 10)]
                    self.left_pinyin_lists += [
                        left_pinyin_list for _ in range(0, len(temp), 10)]
                # update screen
                self.ui.textEdit.clear()
                self.display_candidates(self.page_num)

    def display_candidates(self, page_num: int, last_page_bias=0) -> None:
        """
        Show up to ten candidate Chinese character sequences on screen.

        :param page_num: the number of the page to be shown
        :param last_page_bias: the difference between the previous page number and the current number
        """
        pinyin = "\'".join(self.pinyin_lists[self.page_num])
        last_pinyin = "\'".join(self.pinyin_lists[page_num+last_page_bias])
        # print(last_pinyin,' -> ',pinyin)
        self.ui.lineEdit.setText(pinyin+self.ui.lineEdit.text(
        )[len(last_pinyin):-1])
        for i in range(len(self.candidate[page_num])):
            self.ui.textEdit.append(
                ''.join([str(i) + ': ' + self.candidate[page_num][i] + '\n']))
            self.ui.textEdit.moveCursor(QTextCursor.Start)

    def turn_page(self, step: int) -> None:
        """
        Turn pages of candidate Chinese character sequences.

        :param step: number of pages to be turned
        """
        if 0 <= self.page_num + step < len(self.candidate):
            self.page_num += step
            self.ui.textEdit.clear()
            self.display_candidates(self.page_num, -step)

    def select_candidate(self, num: int) -> None:
        if num < len(self.candidate[self.page_num]):
            text = self.ui.textEdit_2.toPlainText()
            self.ui.textEdit_2.setText(
                text+self.candidate[self.page_num][num])
            self.ui.textEdit.clear()
            if self.left_pinyin_lists[self.page_num]:
                self.ui.lineEdit.setText(self.ui.lineEdit.text(
                )[len("\'".join(self.pinyin_lists[self.page_num][:-len(self.left_pinyin_lists[self.page_num])]))+1:-1])
            else:
                self.ui.lineEdit.setText(self.ui.lineEdit.text()[len(
                    "\'".join(self.pinyin_lists[self.page_num])):-1])

    def keyReleaseEvent(self, e) -> None:
        """
        Function executed when the key is released.
        The self.process function is called every time one key released to realize real-time interaction, and decide whether to turn the page or select a sentence according to the released key.

        :param e: the key just released
        :type e: PyQt5.QtGui.QKeyEvent
        """
        print(type(e))
        if e.key() in [Qt.Key_Left,  Qt.Key_Right]:
            return
        self.process()
        if e.key() == Qt.Key_Equal:
            self.ui.lineEdit.setText(self.ui.lineEdit.text().replace('=', ''))
            self.turn_page(1)  # turn to next page
        elif e.key() == Qt.Key_Minus:
            self.ui.lineEdit.setText(self.ui.lineEdit.text().replace('-', ''))
            self.turn_page(-1)  # turn to previous page
        elif Qt.Key_0 <= e.key() <= Qt.Key_9 or e.key() == Qt.Key_Space:
            if e.key() == Qt.Key_Space:
                num = 0
            else:
                num = e.key()-Qt.Key_0
            self.select_candidate(num)  # select from candidates
            self.process()
