from .database import recoBase3D
from pyqtgraph.Qt import QtGui, QtCore
import numpy
try:
    import pyqtgraph.opengl as gl
except:
    print("Error, must have open gl to use this viewer.")
    exit(-1)

class mchit(recoBase3D):

    """docstring for mchit"""

    def __init__(self):
        super(mchit, self).__init__()
        self._product_name = 'mchit'
        self._gl_points_collection = None
        self._points = None
        self._vals = None



    # this is the function that actually draws the cluster.
    def drawObjects(self, view_manager, event, meta):

        # Get the data from the file:
        _mc_hits = event.mchits()



        self._points = numpy.ndarray((len(_mc_hits),3))
        self._vals   = numpy.ndarray((len(_mc_hits)))
        self._colors = numpy.ndarray((len(_mc_hits),4))
        

        i = 0
        for hit in _mc_hits:
            self._points[i][0] = _mc_hits[i].X
            self._points[i][1] = _mc_hits[i].Y
            self._points[i][2] = _mc_hits[i].Z
            self._vals[i] = _mc_hits[i].E

            i += 1

        
        self._min_coords = numpy.min(self._points, axis=0)
        self._max_coords = numpy.max(self._points, axis=0)

        self.redraw(view_manager)


    def redraw(self, view_manager):


        if self._gl_points_collection is not None:
            view_manager.getView().removeItem(self._gl_points_collection)
            self._gl_points_collection = None

        i = 0
        for val in self._vals:
            this_color = self.getColor(view_manager.getLookupTable(),
                                       view_manager.getLevels(),
                                       val)
            self._colors[i] = this_color
            i += 1

        #make a mesh item: 
        mesh = gl.GLScatterPlotItem(pos=self._points,
                                    color=self._colors,
                                    size=1,
                                    pxMode=False)

        # mesh.setGLOptions("opaque")        
        self._gl_points_collection = mesh
        view_manager.getView().addItem(self._gl_points_collection)

    def getColor(self, _lookupTable, _levels, _voxel_value ):
        _min = _levels[0]
        _max = _levels[1]

        if _voxel_value >= _max:
            return _lookupTable[-1]
        elif _voxel_value < _min:
            return (0,0,0,0)
        else:
            index = 255*(_voxel_value - _min) / (_max - _min)
            return _lookupTable[int(index)]


    def clearDrawnObjects(self, view_manager):
        if self._gl_points_collection is not None:
            view_manager.getView().removeItem(self._gl_points_collection)

        self._gl_points_collection = None
        self._points = None
        self._vals = None
        self._colors = None

    def refresh(self, view_manager):
        self.redraw(view_manager)