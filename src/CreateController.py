#press alt + shift + m 
import maya.cmds as mc

from PySide2.QtWidgets import QWidget

class CreateControllerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create IKFK Limb")
        self.setGeometry(100,100,300,300)

controllerWidget = CreateControllerWidget()
controllerWidget.show()

