

import sys, signal
import argparse
# import collections
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

from view_manager3D import view_manager3D

# Wrap the spin box class to allow key signals to pass to the gui

class ConnectedSpinBox(QtGui.QSpinBox):
    """docstring for ConnectedSpinBox"""
    quitRequested = QtCore.pyqtSignal()
    def __init__(self):
        super(ConnectedSpinBox, self).__init__()
        

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_C:
            # print "C was pressed"
            if e.modifiers() and QtCore.Qt.ControlModifier :
                self.quitRequested.emit()
                return
        else:
            super(ConnectedSpinBox,self).keyPressEvent(e )



class gui3D(QtGui.QWidget):

  def __init__(self):
    super(gui3D, self).__init__()

    # initUI should not do ANY data handling, it should only get the interface loaded
    self._view_manager = view_manager3D()
    # self.setStyleSheet("background-color:rgb(230,230,230);")

  def connect_manager(self,manager):
    self._event_manager = manager

  def closeEvent(self, event):
    self.quit()  

  def quit(self):
    # if self._running:
      # self.stopRun()
    QtCore.QCoreApplication.instance().quit()


  def update(self):
    # set the text boxes correctly:
    self._entryBox.setText(str(self._event_manager.entry()))

    eventLabel = "Ev: " + str(self._event_manager.event())
    self._eventLabel.setText(eventLabel)
    runLabel = "Run: " + str(self._event_manager.run())
    self._runLabel.setText(runLabel)
    # subrunLabel = "Subrun: " + str(self._event_manager.subrun())
    # self._subrunLabel.setText(subrunLabel)
    self._event_manager.drawFresh(self._view_manager)
    

  def updateCameraInfo(self, cameraPos=None,worldPos=None):

    # This function is not for changing the view when the text boxes are changed
    # It is for keeping the text boxes in sync with the view as the user changes the view.

    # UPdate all of the camera text entries:
    if cameraPos is None:
        cameraPos = self._view_manager.getView().cameraPosition()
    if worldPos is None:
        worldPos = self._view_manager.getView().worldCenter()

    # To actually update these things corrently, we have to unplug 
    # the signals from the slots, update the fields, and then plug everything back in
    
    # print self._cameraCenterX.valueChangedf[]


    try:
        self._cameraCenterX.valueChanged.disconnect()
    except:
        pass
    try:
        self._cameraCenterY.valueChanged.disconnect()
    except:
        pass
    try:
        self._cameraCenterZ.valueChanged.disconnect()
    except:
        pass
    try:
        self._worldCenterX.valueChanged.disconnect()
    except:
        pass
    try:
        self._worldCenterY.valueChanged.disconnect()
    except:
        pass
    try:
        self._worldCenterZ.valueChanged.disconnect()
    except:
        pass

    self._cameraCenterX.setValue(cameraPos.x())
    self._cameraCenterY.setValue(cameraPos.y())
    self._cameraCenterZ.setValue(cameraPos.z())
    self._worldCenterX.setValue(worldPos.x())
    self._worldCenterY.setValue(worldPos.y())
    self._worldCenterZ.setValue(worldPos.z())

    self._cameraCenterX.valueChanged.connect(self.cameraCenterWorker)
    self._cameraCenterY.valueChanged.connect(self.cameraCenterWorker)
    self._cameraCenterZ.valueChanged.connect(self.cameraCenterWorker)
    self._worldCenterX.valueChanged.connect(self.worldCenterWorker)
    self._worldCenterY.valueChanged.connect(self.worldCenterWorker)
    self._worldCenterZ.valueChanged.connect(self.worldCenterWorker)


  # This function prepares the buttons such as prev, next, etc and returns a layout
  def getEventControlButtons(self):

    # This is a box to allow users to enter an event (larlite numbering)
    self._goToLabel = QtGui.QLabel("Go to: ")
    self._entryBox = QtGui.QLineEdit()
    self._entryBox.setToolTip("Enter an event to skip to that event (larlite numbering")
    self._entryBox.returnPressed.connect(self.goToEventWorker)
    # # These labels display current events
    self._runLabel = QtGui.QLabel("Run: 0")
    self._eventLabel = QtGui.QLabel("Ev.: 0")
    # self._subrunLabel = QtGui.QLabel("Subrun: 0")

    # Jump to the next event
    self._nextButton = QtGui.QPushButton("Next")
    # self._nextButton.setStyleSheet("background-color: red")
    self._nextButton.clicked.connect(self._event_manager.next)
    self._nextButton.setToolTip("Move to the next event.")
    # Go to the previous event
    self._prevButton = QtGui.QPushButton("Previous")
    self._prevButton.clicked.connect(self._event_manager.prev)
    self._prevButton.setToolTip("Move to the previous event.")

    
    # pack the buttons into a box
    self._eventControlBox = QtGui.QVBoxLayout()

    # Make a horiztontal box for the event entry and label:
    self._eventGrid = QtGui.QHBoxLayout()
    self._eventGrid.addWidget(self._goToLabel)
    self._eventGrid.addWidget(self._entryBox)
    # Another horizontal box for the run/subrun
    # self._runSubRunGrid = QtGui.QHBoxLayout()
    # self._runSubRunGrid.addWidget(self._eventLabel)
    # self._runSubRunGrid.addWidget(self._runLabel)
    # Pack it all together
    self._eventControlBox.addLayout(self._eventGrid)
    self._eventControlBox.addWidget(self._eventLabel)
    self._eventControlBox.addWidget(self._runLabel)
    # self._eventControlBox.addWidget(self._subrunLabel)
    self._eventControlBox.addWidget(self._nextButton)
    self._eventControlBox.addWidget(self._prevButton)

    return self._eventControlBox
  

  # this function helps pass the entry of the line edit item to the event control
  def goToEventWorker(self):
    try:
      event = int(self._entryBox.text())
    except:
      print "Error, must enter an integer"
      self._entryBox.setText(str(self._event_manager.entry()))
      return
    self._event_manager.go_to_entry(event)

  # This function prepares the range controlling options and returns a layout
  def getDrawingControlButtons(self):

    # Button to set range to max
    self._autoRangeButton = QtGui.QPushButton("Auto Range")
    self._autoRangeButton.setToolTip("Set the range of the viewers to show the whole event")
    self._autoRangeButton.clicked.connect(self.autoRangeWorker)


    # add a box to restore the drawing defaults:
    self._restoreDefaults = QtGui.QPushButton("Restore Defaults")
    self._restoreDefaults.setToolTip("Restore the drawing defaults of the views.")
    self._restoreDefaults.clicked.connect(self.restoreDefaultsWorker)


    # self._presetUButton = QtGui.QPushButton("U Plane View")
    # self._presetUButton.setToolTip("Set Camera to mimic the U Plane View")
    # self._presetUButton.clicked.connect(self.goToPresetCameraPosition)
    # self._presetVButton = QtGui.QPushButton("V Plane View")
    # self._presetVButton.setToolTip("Set Camera to mimic the V Plane View")
    # self._presetVButton.clicked.connect(self.goToPresetCameraPosition)
    # self._presetYButton = QtGui.QPushButton("Y Plane View")
    # self._presetYButton.setToolTip("Set Camera to mimic the Y Plane View")
    # self._presetYButton.clicked.connect(self.goToPresetCameraPosition)



    # Add some controls to manage the camera
    self._cameraControlLayout = QtGui.QHBoxLayout()

    # Get the min and max values for height, length, width:

    width  = self._event_manager.meta().max_x() - self._event_manager.meta().min_x()
    height = self._event_manager.meta().max_y() - self._event_manager.meta().min_y()
    length = self._event_manager.meta().max_z() - self._event_manager.meta().min_z()
    

    # Define the x,y,z location of the camera and world center
    self._cameraCenterLayout = QtGui.QVBoxLayout()
    self._cameraLabel = QtGui.QLabel("Camera")
    self._cameraCenterLayout.addWidget(self._cameraLabel)
    self._cameraCenterXLayout = QtGui.QHBoxLayout()
    self._cameraCenterXLabel = QtGui.QLabel("X:")
    self._cameraCenterX = ConnectedSpinBox()
    self._cameraCenterX.setValue(0)
    self._cameraCenterX.setRange(-10*width,10*width)
    self._cameraCenterX.quitRequested.connect(self.quit)
    self._cameraCenterX.valueChanged.connect(self.cameraCenterWorker)
    self._cameraCenterXLayout.addWidget(self._cameraCenterXLabel)
    self._cameraCenterXLayout.addWidget(self._cameraCenterX)

    self._cameraCenterLayout.addLayout(self._cameraCenterXLayout)
    self._cameraCenterYLayout = QtGui.QHBoxLayout()
    self._cameraCenterYLabel = QtGui.QLabel("Y:")
    self._cameraCenterY = ConnectedSpinBox()
    self._cameraCenterY.setValue(0)
    self._cameraCenterY.setRange(-10*height,10*height)
    self._cameraCenterY.quitRequested.connect(self.quit)
    self._cameraCenterY.valueChanged.connect(self.cameraCenterWorker)
    self._cameraCenterYLayout.addWidget(self._cameraCenterYLabel)
    self._cameraCenterYLayout.addWidget(self._cameraCenterY)

    self._cameraCenterLayout.addLayout(self._cameraCenterYLayout)
    self._cameraCenterZLayout = QtGui.QHBoxLayout()
    self._cameraCenterZLabel = QtGui.QLabel("Z:")
    self._cameraCenterZ = ConnectedSpinBox()
    self._cameraCenterZ.setValue(0)
    self._cameraCenterZ.setRange(-10*length,10*length)   
    self._cameraCenterZ.quitRequested.connect(self.quit)
    self._cameraCenterZ.valueChanged.connect(self.cameraCenterWorker)
    self._cameraCenterZLayout.addWidget(self._cameraCenterZLabel)
    self._cameraCenterZLayout.addWidget(self._cameraCenterZ)
    self._cameraCenterLayout.addLayout(self._cameraCenterZLayout)


    self._worldCenterLayout = QtGui.QVBoxLayout()
    self._worldLabel = QtGui.QLabel("world")
    self._worldCenterLayout.addWidget(self._worldLabel)
    self._worldCenterXLayout = QtGui.QHBoxLayout()
    self._worldCenterXLabel = QtGui.QLabel("X:")
    self._worldCenterX = ConnectedSpinBox()
    self._worldCenterX.setValue(0)
    self._worldCenterX.setRange(-10*width,10*width)
    self._worldCenterX.quitRequested.connect(self.quit)
    self._worldCenterX.valueChanged.connect(self.worldCenterWorker)
    self._worldCenterXLayout.addWidget(self._worldCenterXLabel)
    self._worldCenterXLayout.addWidget(self._worldCenterX)

    self._worldCenterLayout.addLayout(self._worldCenterXLayout)
    self._worldCenterYLayout = QtGui.QHBoxLayout()
    self._worldCenterYLabel = QtGui.QLabel("Y:")
    self._worldCenterY = ConnectedSpinBox()
    self._worldCenterY.setValue(0)
    self._worldCenterY.setRange(-10*height,10*height)
    self._worldCenterY.quitRequested.connect(self.quit)
    self._worldCenterY.valueChanged.connect(self.worldCenterWorker)
    self._worldCenterYLayout.addWidget(self._worldCenterYLabel)
    self._worldCenterYLayout.addWidget(self._worldCenterY)

    self._worldCenterLayout.addLayout(self._worldCenterYLayout)
    self._worldCenterZLayout = QtGui.QHBoxLayout()
    self._worldCenterZLabel = QtGui.QLabel("Z:")
    self._worldCenterZ = ConnectedSpinBox()
    self._worldCenterZ.setValue(0)
    self._worldCenterZ.setRange(-10*length,10*length)   
    self._worldCenterZ.quitRequested.connect(self.quit)
    self._worldCenterZ.valueChanged.connect(self.worldCenterWorker)
    self._worldCenterZLayout.addWidget(self._worldCenterZLabel)
    self._worldCenterZLayout.addWidget(self._worldCenterZ)
    self._worldCenterLayout.addLayout(self._worldCenterZLayout)



    # Pack the stuff into a layout

    self._drawingControlBox = QtGui.QVBoxLayout()
    self._drawingControlBox.addWidget(self._restoreDefaults)
    self._drawingControlBox.addWidget(self._autoRangeButton)
    self._drawingControlBox.addLayout(self._cameraControlLayout)

    self._drawingControlBox.addLayout(self._cameraCenterLayout)
    self._drawingControlBox.addLayout(self._worldCenterLayout)

    # self._drawingControlBox.addWidget(self._presetUButton)
    # self._drawingControlBox.addWidget(self._presetVButton)
    # self._drawingControlBox.addWidget(self._presetYButton)


    return self._drawingControlBox

  def worldCenterWorker(self):
    x = float(self._worldCenterX.text())
    y = float(self._worldCenterY.text())
    z = float(self._worldCenterZ.text())
    self._view_manager.setCenter((x,y,z))

  def cameraCenterWorker(self):
    # assemble the camera position:
    x = float(self._cameraCenterX.text())
    y = float(self._cameraCenterY.text())
    z = float(self._cameraCenterZ.text())
    # self.updateCameraInfo(cameraPos=QtGui.QVector3D(x,y,z))
    self._view_manager.setCameraPosition(pos = (x,y,z) )

  def autoRangeWorker(self):
    # Get the list of min/max coordinates:
    _min, _max = self._event_manager.getMinMaxCoords()
    _ctr = 0.5*(_min + _max)
    _diag = (_max - _min) * np.asarray((1.5, 1.5, 1.0))
    self._view_manager.setCenter(_ctr)
    self._view_manager.setCameraPosition(_ctr + _diag)
    # self._view_manager.setCenter((0.0,0.0,0.0))
    # self._view_manager.setCameraPosition(1.5*(_max - _min))
    # # Move the center of the camera to the center of the view:
    # _ctr = 0.5*(_min + _max)
    # print _ctr
    # self._view_manager.pan(_ctr[0], _ctr[1], _ctr[2])

  # def goToPresetCameraPosition(self):
  #   if self.sender() == self._presetUButton:
  #       self._view_manager.setCameraPosition(pos=(0, 500, -500))
  #       print "U Plane"
  #   if self.sender() == self._presetVButton:
  #       self._view_manager.setCameraPosition(pos=(0, 500, 500))
  #       print "V Plane"
  #   if self.sender() == self._presetYButton:
  #       self._view_manager.setCameraPosition(pos=(0, 500, 0))
  #       print "Y Plane"


  def restoreDefaultsWorker(self):
    # self._view_manager.restoreDefaults()
    self._view_manager.setRangeToMax()
    
  # This function prepares the quit buttons layout and returns it
  def getQuitLayout(self):
    self._quitButton = QtGui.QPushButton("Quit")
    self._quitButton.setToolTip("Close the viewer.")
    self._quitButton.clicked.connect(self.quit)
    return self._quitButton

  # This function combines the control button layouts, range layouts, and quit button
  def getWestLayout(self):

    event_control = self.getEventControlButtons()
    draw_control = self.getDrawingControlButtons()


    # Add the quit button?
    quit_control = self.getQuitLayout()
    
    self._westLayout = QtGui.QVBoxLayout()
    self._westLayout.addLayout(event_control)
    self._westLayout.addStretch(1)
    self._westLayout.addLayout(draw_control)
    self._westLayout.addStretch(1)


    self._westLayout.addStretch(1)

    self._westLayout.addWidget(quit_control)
    self._westWidget = QtGui.QWidget()
    self._westWidget.setLayout(self._westLayout)
    self._westWidget.setMaximumWidth(150)
    self._westWidget.setMinimumWidth(100)
    return self._westWidget


  def getSouthLayout(self):
    # This layout contains the status bar and the capture screen buttons

    # The screen capture button:
    self._screenCaptureButton = QtGui.QPushButton("Capture Screen")
    self._screenCaptureButton.setToolTip("Capture the entire screen to file")
    self._screenCaptureButton.clicked.connect(self.screenCapture)
    self._southWidget = QtGui.QWidget()
    self._southLayout = QtGui.QHBoxLayout()
    # Add a status bar
    self._statusBar = QtGui.QStatusBar()
    self._statusBar.showMessage("Test message")
    self._southLayout.addWidget(self._statusBar)
    # self._southLayout.addStretch(1)
    self._southLayout.addWidget(self._screenCaptureButton)
    self._southWidget.setLayout(self._southLayout)

    return self._southWidget

  def getEastLayout(self):
    # This function just makes a dummy eastern layout to use.
    label = QtGui.QLabel("Dummy")
    self._eastWidget = QtGui.QWidget()
    self._eastLayout = QtGui.QVBoxLayout()
    self._eastLayout.addWidget(label)
    self._eastLayout.addStretch(1)
    self._eastWidget.setLayout(self._eastLayout)
    self._eastWidget.setMaximumWidth(200)
    self._eastWidget.setMinimumWidth(100)
    return self._eastWidget

  def refreshEastLayout(self):
    east = getEastLayout()
    self._eastLayout.setVisible(False)
    self._eastLayout.setVisible(True)

  def refreshCenterView(self):

    # for child in self.centerWidget.children():
    #   print type(child)
    #   if type(child) == QtGui.QVBoxLayout:
    #     layout = child

    # print layout.children()
    # print layout

    widget = self._view_manager.getDrawListWidget()
    # for child in widget.children():
    #   print child

    # print widget
    # print layout

    # print layout.children()

    # for i in reversed(range(self.centerWidget.layout.count())): 
        # layout.itemAt(i).widget().setParent(None)

    self.centerWidget.setVisible(False)   
    self.centerWidget.setVisible(True)   


  def metaChanged(self, meta):
    # self._event_manager.meta()refresh_meta()
    self._view_manager.getView().updateMeta(meta)


  def initUI(self):


    # Get all of the widgets:
    self.eastWidget  = self.getEastLayout()
    self.westWidget  = self.getWestLayout()
    self.southLayout = self.getSouthLayout()

    # Area to hold data:
    self._view = self._view_manager.getView()
    self._view.keyPressSignal.connect(self.keyPressEvent)
    self.centerLayout = self._view_manager.getLayout()
    self._view.quitRequested.connect(self.quit)
    self._view.viewChanged.connect(self.updateCameraInfo)

    # Put the layout together


    self.master = QtGui.QVBoxLayout()
    self.slave = QtGui.QHBoxLayout()
    self.slave.addWidget(self.westWidget)
    self.slave.addLayout(self.centerLayout)
    self.slave.addWidget(self.eastWidget)
    self.master.addLayout(self.slave)
    self.master.addWidget(self.southLayout)

    self.setLayout(self.master)    

    # ask the view manager to draw the planes:
    # self._view_manager.drawPlanes(self._event_manager)

    self.updateCameraInfo()

    self.setGeometry(0, 0, 2400, 1600)
    self.setWindowTitle('Event Display')    
    self.setFocus()
    self.show()

  def keyPressEvent(self,e):
    if e.key() == QtCore.Qt.Key_N:
      self._event_manager.next()
      return
    if e.key() == QtCore.Qt.Key_P:
      self._event_manager.prev()
      return
    if e.key() == QtCore.Qt.Key_C:
      # print "C was pressed"
      if e.modifiers() and QtCore.Qt.ControlModifier :
        self.quit()
        return

    # if e.key() == QtCore.Qt.Key_C:
  #     self._dataListsAndLabels['Clusters'].setFocus()
    # if e.key() == QtCore.Qt.Key_H:
  #     self._dataListsAndLabels['Hits'].setFocus()



    super(gui3D, self).keyPressEvent(e)

  def screenCapture(self):
    print("Screen Capture!")
    dialog = QtGui.QFileDialog()
    r = self._event_manager.run()
    e = self._event_manager.event()
    s = self._event_manager.subrun()
    name = "larcv_3D_" + "R" + str(r)
    name = name + "_S" + str(s)
    name = name + "_E" + str(e) + ".png"
    f = dialog.getSaveFileName(self,"Save File",name,
        "PNG (*.png);;JPG (*.jpg);;All Files (*)")

    # print filt
    # Print
    if (pg.Qt.QtVersion.startswith('4')):
      pixmapImage = QtGui.QPixmap.grabWidget(self)
      pixmapImage.save(f,"PNG")
    else:
      pixmapImage = super(gui3D, self).grab()
      pixmapImage.save(f[0],"PNG")



