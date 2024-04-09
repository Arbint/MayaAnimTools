#press alt + shift + m 
import maya.cmds as mc

from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

def CreateBox(name, size):
    pntPositions = ((-0.5,0.5,0.5), (0.5,0.5,0.5), (0.5,0.5,-0.5), (-0.5, 0.5, -0.5), (-0.5, 0.5, 0.5), (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (0.5, -0.5, 0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (0.5, -0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5))
    mc.curve(n = name, d=1, p = pntPositions)
    mc.setAttr(name + ".scale", size, size, size, type = "float3")
    mc.makeIdentity(name, apply = True) # this is freeze transformation
    
def CreateCircleController(jnt, size):
    name = "ac_" + jnt
    mc.circle(n = name, nr=(1,0,0), r = size/2)
    ctrlGrpName = name + "_grp"
    mc.group(name, n = ctrlGrpName)
    mc.matchTransform(ctrlGrpName, jnt)
    mc.orientConstraint(name, jnt)

    return name, ctrlGrpName

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    # this enables Vector + Vector
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
    
    #this enables Vector - Vector 
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    #we are defining Vector * float
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)
    
    #we are defining vector / float
    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar, self.z / scalar)

    def GetLength(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5 

    def GetNormalized(self): 
        return self/self.GetLength()

class CreateLimbControl:
    def __init__(self):
        self.root = ""
        self.mid = ""
        self.end = ""

    def FindJntsBasedOnRootSel(self):
        self.root = mc.ls(sl=True, type = "joint")[0]
        self.mid = mc.listRelatives(self.root, c=True, type="joint")[0]
        self.end = mc.listRelatives(self.mid, c=True, type = "joint")[0]

    def RigLimb(self):
        rootCtrl, rootCtrlGrp = CreateCircleController(self.root, 20)
        midCtrl, midCtrlGrp = CreateCircleController(self.mid, 20)
        endCtrl, endCtrlGrp = CreateCircleController(self.end, 20)

        mc.parent(midCtrlGrp, rootCtrl)
        mc.parent(endCtrlGrp, midCtrl)

        ikEndCtrl = "ac_ik_" + self.end
        CreateBox(ikEndCtrl, 10)
        ikEndCtrlGrp = ikEndCtrl + "_grp"
        mc.group(ikEndCtrl, n = ikEndCtrlGrp)
        mc.matchTransform(ikEndCtrlGrp, self.end)
        mc.orientConstraint(ikEndCtrl, self.end)

        ikHandleName = "ikHandle_" + self.end
        mc.ikHandle(n=ikHandleName, sj = self.root, ee=self.end, sol="ikRPsolver")

        poleVector = mc.getAttr(ikHandleName+".poleVector")[0]
        poleVector = Vector(poleVector[0], poleVector[1], poleVector[2])
        
        print(poleVector)


class CreateLimbControllerWidget(QWidget):
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

        self.autoFindJntDisplay = QLabel("")
        self.masterLayout.addWidget(self.autoFindJntDisplay)
        self.adjustSize()

        rigLimbBtn = QPushButton("Rig Limb")
        rigLimbBtn.clicked.connect(self.RigLimbBtnClicked)
        self.masterLayout.addWidget(rigLimbBtn)

        self.createLimbCtrl = CreateLimbControl()

    def FindJntBtnClicked(self):
        self.createLimbCtrl.FindJntsBasedOnRootSel()
        self.autoFindJntDisplay.setText(f"{self.createLimbCtrl.root},{self.createLimbCtrl.mid},{self.createLimbCtrl.end}")

    def RigLimbBtnClicked(self):
        self.createLimbCtrl.RigLimb()

controllerWidget = CreateLimbControllerWidget()
controllerWidget.show()

