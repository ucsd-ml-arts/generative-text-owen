"""
Visual Questioner GUI.

Image drag-and-drop based on
https://benjaminirving.github.io/blog/2015/09/29/drag-and-drop-files-into-gui-using.

Async processing based on
https://www.learnpyqt.com/courses/concurrent-execution/multithreading-pyqt-applications-qthreadpool.
"""

from __future__ import division, unicode_literals, print_function, absolute_import

import os
import sys
import yaml
import platform
import traceback
from PySide2 import QtGui, QtCore, QtWidgets

op_sys = platform.system()
if op_sys == 'Darwin':
    from Foundation import NSURL

import gpt_2_simple as gpt2
from captioner import Captioner
from postprocess_utils import gpt2_gen_questions

import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

graph = None

class WorkerSignals(QtCore.QObject):
    finished = QtCore.Signal()
    error = QtCore.Signal(tuple)
    result = QtCore.Signal(str)

class Worker(QtCore.QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @QtCore.Slot()
    def run(self):
        try:
            question = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(question)
        finally:
            self.signals.finished.emit()

class WindowWidget(QtWidgets.QWidget):
    def __init__(self):
        super(WindowWidget, self).__init__()
        self.sess = None
        self.captioner = None
        self.prepare_questioner()
        self.prepare_captioner()
        self.threadpool = QtCore.QThreadPool()
        self.questioner_running = False

        global graph
        graph = tf.get_default_graph()

        # Viewing region
        self.viewing_region = QtWidgets.QLabel(self)
        layout = QtWidgets.QHBoxLayout()
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

    def prepare_questioner(self):
        self.sess = gpt2.start_tf_sess()
        gpt2.load_gpt2(self.sess)

    def prepare_captioner(self):
        config = yaml.load(open('config.yaml', 'r'), Loader=yaml.FullLoader)
        checkpoint_path = os.path.join(config['project_root_dir'], config['checkpoint_path'])
        vocab_file_path = os.path.join(config['project_root_dir'], config['vocab_file_path'])
        self.captioner = Captioner(self.sess, checkpoint_path, vocab_file_path)
    
    def load_button_clicked(self):
        if self.questioner_running:
            print("Can't load an image right now. Questioner is busy.")
        else:
            image_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file')
            if image_path:
                self.load_image(image_path)
    
    def load_image(self, image_path):
        pixmap = QtGui.QPixmap(image_path)
        pixmap = pixmap.scaled(500, 500, QtCore.Qt.KeepAspectRatio)
        self.viewing_region.setPixmap(pixmap)
        self.text_region.setText('Questioner is working.')

        self.questioner_running = True
        worker = Worker(self.run_questioner, image_path)
        worker.signals.finished.connect(self.questioner_finished)
        worker.signals.error.connect(self.questioner_failed)
        worker.signals.result.connect(self.apply_questioner_output)
        self.threadpool.start(worker)

    def run_questioner(self, image_path):
        global graph
        with graph.as_default():  # this is run on a separate thread
            caption = self.captioner.caption(image_path)
            questions = gpt2_gen_questions(
                self.sess, caption, nsamples=1, temperature=0.7)
            return questions[0] if len(questions) > 0 else ''

    def questioner_finished(self):
        self.questioner_running = False

    def questioner_failed(self, e):
        print(e)

    def apply_questioner_output(self, question):
        if len(question) > 0:
            self.text_region.setText(question)
    
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
        if evt.mimeData().hasUrls and not self.questioner_running:
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
