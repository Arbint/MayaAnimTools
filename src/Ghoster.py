import maya.cmds as mc
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QAbstractItemView

class Ghost:
    def __init__(self):
        self.srcMeshes = set() # a set is a list that has unique elements.

    def SetSelectedAsSrcMesh(self):
        selection = mc.ls(sl=True)
        self.srcMeshes.clear() # removes all elements in the set.
        for selected in selection:
            shapes = mc.listRelatives(selected, s=True) # find all shapes of the selected object
            for s in shapes:
                if mc.objectType(s) == "mesh": # the object is a mesh
                    self.srcMeshes.add(selected) # add the mesh to our set.

class GhostWidget(QWidget):
    def __init__(self):
        super().__init__() # needed to call if you are inheriting from a parent class
        self.ghost = Ghost() # create a ghost to pass command to.
        self.setWindowTitle("Ghoster Poser V1.0") # set the title of the window
        self.masterLayout = QVBoxLayout() # creates a vertical layout         
        self.setLayout(self.masterLayout) # tells the window to use the vertical layout created in the previous line

        self.srcMeshList = QListWidget() # create a list to show stuff.
        self.srcMeshList.setSelectionMode(QAbstractItemView.ExtendedSelection) # allow multi-seleciton
        self.masterLayout.addWidget(self.srcMeshList) # this adds the list created previously to the layout.

        addSrcMeshBtn = QPushButton("Add Source Mesh")
        addSrcMeshBtn.clicked.connect(self.AddSrcMeshBtnClicked)
        self.masterLayout.addWidget(addSrcMeshBtn)

    def AddSrcMeshBtnClicked(self):
        self.ghost.SetSelectedAsSrcMesh() # asks ghost to populate it's srcMeshes with the current selection
        self.srcMeshList.clear() # this clears our list widget
        self.srcMeshList.addItems(self.ghost.srcMeshes) # this add the srcMeshes collected eariler to the list widget

ghostWidget = GhostWidget()
ghostWidget.show()