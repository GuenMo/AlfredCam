# coding:utf-8

import os
from PySide import QtGui, QtCore
from shiboken import wrapInstance

import pymel.all as pm
from functools import partial
from logo import Logo
import maya.OpenMayaUI as OpenMayaUI
import stylesheet

import alfredCam as Camera
reload(Camera)
import resources
reload(resources)

__version__ = '1.1.0'

def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtGui.QMainWindow)

def mayaToQtObject( inMayaUI ):
    ptr = OpenMayaUI.MQtUtil.findControl( inMayaUI )
    if ptr is None:
        ptr = OpenMayaUI.MQtUtil.findLayout( inMayaUI )
    if ptr is None:
        ptr= OpenMayaUI.MQtUtil.findMenuItem( inMayaUI )
    if ptr is not None:
        return wrapInstance( long( ptr ), QtGui.QWidget )

class MainWindow(QtGui.QMainWindow):
    
    def __init__(self, parent=getMayaWindow()):
        super(MainWindow, self).__init__(parent)
        
        self.camera    = Camera.TumbleCamera()
        
        self.rootPath  = MainWindow.getRootPath()
        self.imagePath = MainWindow.getImagePath()
        self.stylData  = stylesheet.darkorange

        self.initUi()
        self.connections()
        self.checkAttr()
        self.createCameraScriptJob()
        
    def initUi(self):
        self.logo = Logo()
        self.mayaWiget = pm.text()
        self.mayaText = mayaToQtObject(self.mayaWiget)
        self.setWindowTitle('Alfred Camera Tool')
        self.centralWidget = QtGui.QWidget()
        self.setCentralWidget(self.centralWidget)
        self.mainLayoyt = QtGui.QVBoxLayout()
        self.centralWidget.setLayout(self.mainLayoyt)
        
        # Create Camera UI
        self.creationGroup  = QtGui.QGroupBox('Create')
        self.creationLayout = QtGui.QGridLayout()
        self.creationGroup.setLayout(self.creationLayout)
        
        cameraNameLabel = QtGui.QLabel('Camera Name:')
        cameraNameLabel.setAlignment(QtCore.Qt.AlignRight)
        self.cameraLineEdit = QtGui.QLineEdit()
        self.createCameraPushBtn = QtGui.QPushButton('Create Camera')
        
        self.creationLayout.addWidget(cameraNameLabel,         0,0)
        self.creationLayout.addWidget(self.cameraLineEdit,     0,1)
        self.creationLayout.addWidget(self.createCameraPushBtn,1,1)
        
        # Edit Camera UI
        self.editGroup  = QtGui.QGroupBox('Edit')
        self.editLayout = QtGui.QGridLayout()
        self.editGroup.setLayout(self.editLayout)
        
        renameLabel         = QtGui.QLabel('Camera Rename:')
        self.renameLineEdit = QtGui.QLineEdit()
        self.renameButton   = QtGui.QPushButton('Rename')
        matchFilmLabel      = QtGui.QLabel('Match Filmback \nto Resolution:')
        matchFilmLabel.setWordWrap(True)
        self.matchButton    = QtGui.QPushButton('Match')
        setRangeLabel       = QtGui.QLabel('Set Playback \nRange of Camera:')
        setRangeLabel.setWordWrap(True)
        self.setRangeButton = QtGui.QPushButton('Set Range')
        
        self.editLayout.addWidget(renameLabel,         0,0)
        self.editLayout.addWidget(self.renameLineEdit, 0,1)
        self.editLayout.addWidget(self.renameButton,   1,1)
        self.editLayout.addWidget(matchFilmLabel,      2,0)
        self.editLayout.addWidget(self.matchButton,    2,1)
        self.editLayout.addWidget(setRangeLabel,       4,0)
        self.editLayout.addWidget(self.setRangeButton, 4,1)
        
        # Operation
        self.operationGroup  = QtGui.QGroupBox('Operation')
        operationLayout = QtGui.QHBoxLayout()
        self.renderableButton = QtGui.QPushButton('Renderable')
        self.bakeButton = QtGui.QPushButton('Bake')
        self.deleteButton = QtGui.QPushButton('Delete')
        operationLayout.addWidget(self.renderableButton)
        operationLayout.addWidget(self.bakeButton)
        operationLayout.addWidget(self.deleteButton)
        self.operationGroup.setLayout(operationLayout)
        
        #self.mainLayoyt.addWidget(self.logo)
        self.mainLayoyt.addWidget(self.creationGroup)
        self.mainLayoyt.addWidget(self.editGroup)
        self.mainLayoyt.addWidget(self.operationGroup)
        self.mainLayoyt.addWidget(self.mayaText)
        self.mayaText.setVisible(False)
        self.mainLayoyt.addStretch()

        self.status = self.statusBar()
        
        self.setDefaultUI()
        
        #Set Window
        windowLogoImage = QtGui.QPixmap(os.path.join(self.imagePath,'camera.png'))
        windowLogoIcon  = QtGui.QIcon(windowLogoImage)
        self.setWindowIcon(windowLogoIcon)
        self.setFixedWidth(300)
        self.setStyleSheet(self.stylData)
        self.setObjectName('alfredCamUI')
        
    def connections(self):
        self.createCameraPushBtn.clicked.connect(self.createCamera)
        self.renameButton.clicked.connect(self.renameCamera)
        self.matchButton.clicked.connect(self.matchFilmback)
        self.setRangeButton.clicked.connect(self.setRange)
        self.renderableButton.clicked.connect(self.setRanderable)
        self.bakeButton.clicked.connect(self.bakeCamera)
        self.deleteButton.clicked.connect(self.deleteCamera)
        
    def setDefaultUI(self):
        self.cameraLineEdit.setText('camera1')
        self.editGroup.setEnabled(False)
        
    def createCamera(self):
        cameraName = self.cameraLineEdit.text()
        if self.camera.find(cameraName):
            self.printStaus('exists')
            return
        # Create camera
        camera = self.camera.create(cameraName)
        # Create control
        cameraCtrl = self.camera.createCtrl(cameraName)
        # Set Default 
        self.camera.setDefault(cameraCtrl)
        self.camera.matchFilmBackToResolution(camera[1])
        self.camera.setCameraForBig(cameraCtrl, camera[1])
        # Create expression
        self.camera.createExpression(camera[0], cameraCtrl)
        self.camera.createMeta(camera[0].name())
        #self.camera.lockNodes()
        self.printStaus('create')
        
    def renameCamera(self):
        if self.renameLineEdit.text() == '':
            self.printStaus('none')
            return
        if self.camera.find(self.renameLineEdit.text()):
            self.printStaus('exists')
            return
        
        self.camera.rename(self.renameLineEdit.text())
        self.printStaus('rename')
        
    def matchFilmback(self):
        self.camera.setMatch()
        self.printStaus('match')
        
    def setRange(self):
        self.camera.setRange()
        self.printStaus('range')
        
    def printStaus(self, case):
        if case == 'exists':
            self.status.setStyleSheet("QStatusBar{color:red;font-weight:bold;}")
            self.status.showMessage(u'같은 이름이 카메라가 존재합니다.', 3000)
        if case == 'create':
            self.status.setStyleSheet("QStatusBar{color:yellow;font-weight:bold;}")
            self.status.showMessage(u'{}가 만들어 졌습니다.'.format(self.cameraLineEdit.text()), 3000)
        if case == 'none':
            self.status.setStyleSheet("QStatusBar{color:red;font-weight:bold;}")
            self.status.showMessage(u'새로운 이름을 입력하세요.', 3000)
        if case == 'renderable':
            self.status.setStyleSheet("QStatusBar{color:yellow;font-weight:bold;}")
            self.status.showMessage(u'렌더 카메라로 설정 되었습니다.', 3000)
        if case == 'bake':
            self.status.setStyleSheet("QStatusBar{color:yellow;font-weight:bold;}")
            self.status.showMessage(u'카메라가 베이크 되었습니다.', 3000)
        if case == 'delete':
            self.status.setStyleSheet("QStatusBar{color:yellow;font-weight:bold;}")
            self.status.showMessage(u'카메라가 삭제 되었습니다.', 3000)
        if case == 'rename':
            self.status.setStyleSheet("QStatusBar{color:yellow;font-weight:bold;}")
            self.status.showMessage(u'카메라의 이름을 바꾸었습다.', 3000)
        if case == 'match':
            self.status.setStyleSheet("QStatusBar{color:yellow;font-weight:bold;}")
            self.status.showMessage(u'카메라의 "Aperture" 속성 값이 [1.778, 1.000]으로 설정 되었습니다.', 3000)
        if case == 'range':
            self.status.setStyleSheet("QStatusBar{color:yellow;font-weight:bold;}")
            self.status.showMessage(u'타임 레인지가 설정 되었습니다.', 3000)
        
    def closeEvent(self, event):
        self.deleteCamreaScriptJob()

    def checkAttr(self):
        sels = pm.ls(sl=True)
        print sels
        if sels and len(sels) == 1:
            if self.camera.isTumbleCamera(sels[0]):
                self.upDateUI(False)
            else:
                self.upDateUI(True)
        else:
            self.upDateUI(True)

    def createCameraScriptJob(self):
        self.jobNum = pm.scriptJob(event=['SelectionChanged', partial(self.checkAttr)], protected=True, parent=self.mayaWiget)
        
    def deleteCamreaScriptJob(self):
        pm.scriptJob(kill=self.jobNum, force=True)
        
    def upDateUI(self, state):
        self.creationGroup.setEnabled(state)
        self.editGroup.setEnabled(not state)
        self.operationGroup.setEnabled(not state)

        self.creationGroup.setVisible(state)
        self.editGroup.setVisible(not state)
        self.operationGroup.setVisible(not state)
        
        if state:
            self.setFixedSize(300, 122)
        else:
            self.setFixedSize(300, 262)
    
    def setRanderable(self):
        self.camera.setRenderable()
        self.printStaus('renderable')
        
    def bakeCamera(self):
        self.camera.bake()
        self.printStaus('bake')
        
    def deleteCamera(self):
        reply = QtGui.QMessageBox.question(self, 
                                           'Delete Camera',
                                           u'선택된 카메라를 삭제 하시겠습니까?',
                                           QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        
        if reply == QtGui.QMessageBox.Yes:
            self.camera.delete()
            self.printStaus('delete')
        else:
            return
        
    @staticmethod
    def getRootPath():
        return os.path.dirname(__file__)
    
    @staticmethod
    def getImagePath():
        return os.path.join(MainWindow.getRootPath(),'images')
        
def main():
    global win
    try:
        win.close()
        win.deleteLater()
    except: 
        pass
    win = MainWindow()
    win.show()
