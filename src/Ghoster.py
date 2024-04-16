import maya.cmds as mc
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QAbstractItemView

class GhostWidget(QWidget):
    def __init__(self):
        super().__init__() # needed to call if you are inheriting from a parent class
        
