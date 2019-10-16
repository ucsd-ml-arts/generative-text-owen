"""
Visual Questioner GUI.
Image drag-and-drop based on
https://benjaminirving.github.io/blog/2015/09/29/drag-and-drop-files-into-gui-using.
"""

from __future__ import division, unicode_literals, print_function, absolute_import

import os
import sys
import platform
from PySide2 import QtGui, QtCore, QtWidgets

op_sys = platform.system()
if op_sys == 'Darwin':
    from Foundation import NSURL

class WindowWidget(QtWidgets.QWidget):
    def __init__(self):
        super(WindowWidget, self).__init__()
        layout = QtWidgets.QHBoxLayout()

        # Viewing region
        self.viewing_region = QtWidgets.QLabel(self)
        layout.addWidget(self.viewing_region)

        # Load button
        self.load_button = QtWidgets.QPushButton('Load image')
        self.load_button.clicked.connect(self.load_button_clicked)
        right_sidebar = QtWidgets.QVBoxLayout()
        right_sidebar.addWidget(self.load_button)

        # Extra instructions region
        self.instr_region = QtWidgets.QLabel(self)
        self.instr_region.setText('Or drop an image onto this window.')
        right_sidebar.addWidget(self.instr_region)
        right_sidebar.addStretch()

        # Text region
        self.text_region = QtWidgets.QLabel(self)
        self.text_region.setFrameStyle(
            QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
        self.text_region.setWordWrap(True)
        self.text_region.setMargin(8)
        self.text_region.setText('...')
        right_sidebar.addWidget(self.text_region)
        layout.addLayout(right_sidebar)

        # Launch
        self.setWindowIcon(QtGui.QIcon(os.path.join('icon', 'question.png')))
        self.setLayout(layout)
        self.setAcceptDrops(True)
        self.show()
    
    def load_button_clicked(self):
        image_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file')
        self.load_image(image_path)
    
    def load_image(self, image_path):
        pixmap = QtGui.QPixmap(image_path)
        pixmap = pixmap.scaled(500, 500, QtCore.Qt.KeepAspectRatio)
        self.viewing_region.setPixmap(pixmap)
    
    def dragEnterEvent(self, evt):
        if evt.mimeData().hasUrls:
            evt.accept()
        else:
            evt.ignore()
    
    def dragMoveEvent(self, evt):
        if evt.mimeData().hasUrls:
            evt.accept()
        else:
            evt.ignore()
    
    def dropEvent(self, evt):
        if evt.mimeData().hasUrls:
            evt.setDropAction(QtCore.Qt.CopyAction)
            evt.accept()
            for url in evt.mimeData().urls():
                if op_sys == 'Darwin':
                    image_path = str(NSURL.URLWithString_(str(url.toString())).filePathURL().path())
                else:
                    image_path = str(url.toLocalFile())
            self.load_image(image_path)
        else:
            evt.ignore()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    _ = WindowWidget()
    sys.exit(app.exec_())
