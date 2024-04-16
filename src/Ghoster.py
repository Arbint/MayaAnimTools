import maya.cmds as mc
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QAbstractItemView

def GetCurrentFrame():
    return int(mc.currentTime(query=True))

class Ghost:
    def __init__(self):
        self.srcMeshes = set() # a set is a list that has unique elements.
        self.ghostGrp = "ghost_grp"
        self.frameAttr = "frame"
        self.srcAttr = "src"

        self.InitIfGhostGrpNotExist()

    def InitIfGhostGrpNotExist(self):
        if mc.objExists(self.ghostGrp):
            storedSrcMeshes = mc.getAttr(self.ghostGrp + "." + self.srcAttr)
            self.srcMeshes = set(storedSrcMeshes.split(","))
            return
        
        mc.createNode("transform", n = self.ghostGrp)
        mc.addAttr(self.ghostGrp, ln = self.srcAttr, dt="string")

        
    def SetSelectedAsSrcMesh(self):
        selection = mc.ls(sl=True)
        self.srcMeshes.clear() # removes all elements in the set.
        for selected in selection:
            shapes = mc.listRelatives(selected, s=True) # find all shapes of the selected object
            for s in shapes:
                if mc.objectType(s) == "mesh": # the object is a mesh
                    self.srcMeshes.add(selected) # add the mesh to our set.

        mc.setAttr(self.ghostGrp + "." + self.srcAttr, ",".join(self.srcMeshes), type = "string")

    def AddGhost(self):
        for srcMesh in self.srcMeshes:
            currentFrame = GetCurrentFrame()
            ghostName = srcMesh + "_" + str(currentFrame)
            if mc.objExists(ghostName):
                mc.delete(ghostName)

            mc.duplicate(srcMesh, n = ghostName)
            mc.parent(ghostName, self.ghostGrp)
            mc.addAttr(ghostName, ln = self.frameAttr, dv = currentFrame)

    def GoToNextGhost(self):
        frames = self.GetGhostFramesSorted() # find all the frames we have in ascending order
        if not frames: # if theres is not frames, there is not ghost, do nothing
            return

        currentFrame = GetCurrentFrame()        
        for frame in frames: #go through each frame
            if frame > currentFrame: #if we find one that is bigger than the current frame, it should be where we move time slider to.
                mc.currentTime(frame, e=True) # e means edit, we are editing the time slider to be at frame
                return
        
        mc.currentTime(frames[0], e=True) # found no frame bigger, got to the beginning

    def GoToPrevGhost(self):
        # to go backwards, you can use the frames.reverse(), it will reverse frames make it in decending order.
        pass

    def GetGhostFramesSorted(self):
        frames = set()
        ghosts = mc.listRelatives(self.ghostGrp, c=True)
        if not ghosts:
            return []
        
        for ghost in ghosts:
            frame = mc.getAttr(ghost + "." + self.frameAttr)
            frames.add(frame)

        frames = list(frames) # this converts frames to a list
        frames.sort() # this sorts the frames list to ascending order
        return frames # returns the sorted frames

class GhostWidget(QWidget):
    def __init__(self):
        super().__init__() # needed to call if you are inheriting from a parent class
        self.ghost = Ghost() # create a ghost to pass command to.
        self.setWindowTitle("Ghoster Poser V1.0") # set the title of the window
        self.masterLayout = QVBoxLayout() # creates a vertical layout         
        self.setLayout(self.masterLayout) # tells the window to use the vertical layout created in the previous line

        self.srcMeshList = QListWidget() # create a list to show stuff.
        self.srcMeshList.setSelectionMode(QAbstractItemView.ExtendedSelection) # allow multi-seleciton
        self.srcMeshList.itemSelectionChanged.connect(self.SrcMeshSelectionChanged)
        self.srcMeshList.addItems(self.ghost.srcMeshes)
        self.masterLayout.addWidget(self.srcMeshList) # this adds the list created previously to the layout.

        addSrcMeshBtn = QPushButton("Add Source Mesh")
        addSrcMeshBtn.clicked.connect(self.AddSrcMeshBtnClicked)
        self.masterLayout.addWidget(addSrcMeshBtn)

        self.ctrlLayout = QHBoxLayout()
        self.masterLayout.addLayout(self.ctrlLayout)

        addGhostBtn = QPushButton("Add/Update")
        addGhostBtn.clicked.connect(self.ghost.AddGhost)
        self.ctrlLayout.addWidget(addGhostBtn)

        prevGhostBtn = QPushButton("Prev")
        prevGhostBtn.clicked.connect(self.ghost.GoToPrevGhost)
        self.ctrlLayout.addWidget(prevGhostBtn)

        nextGhostBtn = QPushButton("Next")
        nextGhostBtn.clicked.connect(self.ghost.GoToNextGhost)
        self.ctrlLayout.addWidget(nextGhostBtn)


    def SrcMeshSelectionChanged(self):
        mc.select(cl=True) # this deselect everything.
        for item in self.srcMeshList.selectedItems():
            mc.select(item.text(), add = True)

    def AddSrcMeshBtnClicked(self):
        self.ghost.SetSelectedAsSrcMesh() # asks ghost to populate it's srcMeshes with the current selection
        self.srcMeshList.clear() # this clears our list widget
        self.srcMeshList.addItems(self.ghost.srcMeshes) # this add the srcMeshes collected eariler to the list widget

ghostWidget = GhostWidget()
ghostWidget.show()