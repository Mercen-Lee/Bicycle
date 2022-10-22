# Bicycle IDLE

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
import io, os, sys, bicycle

class MainClass(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(580,400)
        self.setWindowTitle('자전거 IDLE')
        self.font = QFont()
        self.fontsize = 20
        self.font.setPointSize(self.fontsize)
        self.codeEdit = QTextEdit(self)
        self.codeEdit.setFont(self.font)
        self.codeEdit.setStyleSheet('background: rgba(253,253,253); color: black;')
        self.codeExec = QTextEdit(self)
        self.codeExec.setFont(self.font)
        self.codeExec.setStyleSheet('background: rgba(253,253,253); color: black;')
        self.codeBox = QVBoxLayout()
        self.codeBox.addWidget(self.codeEdit)
        self.codeBox.addWidget(self.codeExec)
        self.setLayout(self.codeBox)
        self.setStyleSheet('background: rgba(236,236,236);')
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_F5:
            self.codeExec.clear()
            r = bicycle.Transfile(self.codeEdit.toPlainText())
            print(r)
            old_stdout = sys.stdout
            redirected_output = sys.stdout = io.StringIO()
            exec(r.lstrip())
            sys.stdout = old_stdout
            self.codeExec.append(redirected_output.getvalue())

        elif e.key() == Qt.Key_Equal and e.modifiers() & Qt.ControlModifier:
            self.fontsize += 4
            self.font.setPointSize(self.fontsize)
            self.codeEdit.setFont(self.font)
            self.codeExec.setFont(self.font)
        elif e.key() == Qt.Key_Minus and e.modifiers() & Qt.ControlModifier:
            self.fontsize -= 4
            self.font.setPointSize(self.fontsize)
            self.codeEdit.setFont(self.font)
            self.codeExec.setFont(self.font)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MainClass()
    myWindow.show()
    app.exec_()
