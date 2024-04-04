#press alt + shift + m 
import maya.cmds as mc

from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class CreateControllerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create IKFK Limb")
        self.setGeometry(100,100,300,300)
        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)

        hintLabel = QLabel("Please Select the root of the limb:")
        self.masterLayout.addWidget(hintLabel)

        findJntsBtn = QPushButton("Find Jnts")
        findJntsBtn.clicked.connect(self.FindJntBtnClicked)

        self.masterLayout.addWidget(findJntsBtn)
        self.adjustSize()

    def FindJntBtnClicked(self):
        print("I am clicked")





controllerWidget = CreateControllerWidget()
controllerWidget.show()

