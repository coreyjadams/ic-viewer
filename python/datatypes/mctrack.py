from .database import recoBase3D
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import numpy
try:
    import pyqtgraph.opengl as gl
except:
    print("Error, must have open gl to use this viewer.")
    exit(-1)

class mctrack(recoBase3D):

    """docstring for mctrack"""

    def __init__(self):
        super(mctrack, self).__init__()
        self._product_name = 'mctrack'
        self._gl_points_collection = None
        self._points = None
        self._vals = None



    # this is the function that actually draws the cluster.
    def drawObjects(self, view_manager, event, meta):

        # Get the data from the file:
        _mc_tracks = event.mctracks()


        _running_min = None
        _running_max = None
        for track in _mc_tracks:

            # construct a line for this track:
            points = track.GetHits()
            x = numpy.zeros(points.size())
            y = numpy.zeros(points.size())
            z = numpy.zeros(points.size())

            i = 0
            for point in points:
                x[i] = point.GetPosition().x()
                y[i] = point.GetPosition().y()
                z[i] = point.GetPosition().z()
                i+= 1

            pts = numpy.vstack([x,y,z]).transpose()

            _this_min = numpy.min(pts, axis=0)
            _this_max = numpy.max(pts, axis=0)

            if _running_min is None:
                _running_min = _this_min
            else:
                _running_min = numpy.minimum(_this_min, _running_min)
            if _running_max is None:
                _running_max = _this_max
            else:
                _running_max = numpy.maximum(_this_max, _running_max)


            pen = pg.mkPen((255,0,0), width=3)
            line = gl.GLLinePlotItem(pos=pts,color=(255,255,0,255))
            view_manager.getView().addItem(line)
            self._drawnObjects.append(line)

        self._min_coords = _running_min
        self._max_coords = _running_max
