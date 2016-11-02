# coding:utf-8

try:
    import PySide
    from PySide.QtGui import *
    from PySide.QtCore import *
    from shiboken import wrapInstance
except:
    import PySide2
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance
import os, sys

class Logo(QLabel):
    
    APPDIR =  os.path.dirname(__file__)
    IMAGESDIR = os.path.join(APPDIR,'images')
    
    def __init__(self, parent=None):
        super(Logo, self).__init__(parent)
        logoImage = QPixmap(os.path.join(self.IMAGESDIR, 'logo.png'))
        self.setAlignment(Qt.AlignRight)
        self.setPixmap(logoImage.scaled(150,50, Qt.KeepAspectRatio))
        # Set Widget
        self.setWindowTitle("Logo")
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Logo()
    ui.show()
    sys.exit(app.exec_())