# coding:utf-8

from PySide import QtGui, QtCore
import os, sys

class Logo(QtGui.QLabel):
    
    APPDIR =  os.path.dirname(__file__)
    IMAGESDIR = os.path.join(APPDIR,'images')
    
    def __init__(self, parent=None):
        super(Logo, self).__init__(parent)
        logoImage = QtGui.QPixmap(os.path.join(self.IMAGESDIR, 'logo.png'))
        self.setAlignment(QtCore.Qt.AlignRight)
        self.setPixmap(logoImage.scaled(150,50, QtCore.Qt.KeepAspectRatio))
        # Set Widget
        self.setWindowTitle("Logo")
    
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ui = Logo()
    ui.show()
    sys.exit(app.exec_())