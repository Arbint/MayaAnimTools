import maya.cmds as mc
from PySide2.QtWidgets import QLineEdit, QMessageBox, QPushButton, QVBoxLayout, QWidget

class MayaToUE:
    def __init__(self):
        self.rootJnt = ""
        self.meshes = set()
        self.fileName = ""
        self.animations = []
        self.saveDir = ""

    def SetSelectedAsRootJnt(self):
        selection = mc.ls(sl = True, type = "joint")
        if not selection:
            return False, "No Joint Selected" 

        self.rootJnt = selection[0]
        return True, ""

    def SetSelectedAsMeshes(self):
        selection = mc.ls(sl=True)
        if not selection:
            return False, "No Mesh Selected"
        
        meshes = set() # creates a local variable of the type set
        for sel in selection: # loop through everything we select
            shapes = mc.listRelatives(sel, s=True) # find their shape nodes
            for s in shapes: # for each shape node we find
                if mc.objectType(s) == "mesh": #check if there are mesh shapes.
                    meshes.add(sel) # if they are mesh shapes, we will collect them

        if len(meshes) == 0:
            return False, "No Mesh Selected"
        
        self.meshes = meshes
        return True, ""
        

class MayaToUEWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.mayaToUE = MayaToUE()
        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)

        self.jointLineEdit = QLineEdit()
        self.jointLineEdit.setEnabled(False) # make it grayed out.
        self.masterLayout.addWidget(self.jointLineEdit)

        setSelectedAsRootJntBtn = QPushButton("Set Selected As Root Joint")
        setSelectedAsRootJntBtn.clicked.connect(self.SetSelectedAsRootBtnClicked)
        self.masterLayout.addWidget(setSelectedAsRootJntBtn)

    def SetSelectedAsRootBtnClicked(self):
        success, msg = self.mayaToUE.SetSelectedAsRootJnt()
        if success:
            self.jointLineEdit.setText(self.mayaToUE.rootJnt)
        else:
            QMessageBox().warning(self, "Warning", msg)

mayaToUEWidget = MayaToUEWidget()
mayaToUEWidget.show()
