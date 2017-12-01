try:
    import pyqtgraph.opengl as gl
except:
    print("ERROR: Must have opengl for this display.")

from .gui3D import gui3D
from pyqtgraph.Qt import QtGui, QtCore
from manager import evd_manager_3D


# Inherit the basic gui to extend it
# override the gui to give the display special features:


class evdgui3D(gui3D):

    """special larlite gui for 3D"""

    def __init__(self, mgr):
        super(evdgui3D, self).__init__(mgr)
        self._event_manager.eventChanged.connect(self.update)
        self._view_manager.refreshColors.connect(self.refreshColors)


    # override the initUI function to change things:
    def initUI(self):
        super(evdgui3D, self).initUI()
        # self.metaChanged(self._event_manager.io_manager())
        self._view_manager.setRangeToMax()

        # Change the name of the labels for lariat:
        self.update()

    def refreshColors(self):
        self._event_manager.refreshColors(self._view_manager)

    # This function sets up the eastern widget
    def getEastLayout(self):
        # This function just makes a dummy eastern layout to use.
        label1 = QtGui.QLabel("NEXT")
        label2 = QtGui.QLabel("EVD 3D")
        font = label1.font()
        font.setBold(True)
        label1.setFont(font)
        label2.setFont(font)

        self._eastWidget = QtGui.QWidget()
        # This is the total layout
        self._eastLayout = QtGui.QVBoxLayout()
        # add the information sections:
        self._eastLayout.addWidget(label1)
        self._eastLayout.addWidget(label2)
        self._eastLayout.addStretch(1)
        
        # self._paramsDrawBox = QtGui.QCheckBox("Draw Params.")
        # self._paramsDrawBox.stateChanged.connect(self.paramsDrawBoxWorker)
        # self._eastLayout.addWidget(self._paramsDrawBox)
        # self._eastLayout.addStretch(1)

        # In this case, many things are not made with different producers
        # but just exist.  So use check boxes to toggle them on and off.

        # Now we get the list of items that are drawable:
        drawableProducts = self._event_manager.getDrawableProducts()

        for product in drawableProducts:
            thisBox = QtGui.QCheckBox(product)
            thisBox.stateChanged.connect(self.checkBoxHandler)
            self._eastLayout.addWidget(thisBox)


        self._eastLayout.addStretch(2)

        self._eastWidget.setLayout(self._eastLayout)
        self._eastWidget.setMaximumWidth(150)
        self._eastWidget.setMinimumWidth(100)
        return self._eastWidget

    def drawableProductsChanged(self):
        # self.removeItem(self._eastLayout)
        self._eastWidget.close()
        east = self.getEastLayout()
        self.slave.addWidget(east)
        self.update()


    def recoBoxHandler(self, text):
        sender = self.sender()
        # print sender.product(), "was changed to" , text
        if text == "--Select--" or text == "--None--":
            self._event_manager.redrawProduct(sender.name(), None, self._view_manager)
            return
        else:
            self._event_manager.redrawProduct(sender.name(), text, self._view_manager)


    def checkBoxHandler(self, state):
        sender = self.sender()
        if not sender.isChecked():
            self._event_manager.redrawProduct(str(sender.text()), self._view_manager, draw=False)
            return
        else:
            self._event_manager.redrawProduct(str(sender.text()), self._view_manager, draw=True)

