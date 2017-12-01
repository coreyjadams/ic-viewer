# This is the class that maintains the list of drawable items.
# If your class isn't here, it can't be drawn
import collections

import pyqtgraph.opengl as gl
from .mchit import mchit
from .mctrack import mctrack
from .pmap import pmap
from .cluster import cluster

class drawableItems3D(object):

    """This class exists to enumerate the drawableItems in 3D"""
    # If you make a new drawing class, add it here

    def __init__(self):
        super(drawableItems3D, self).__init__()
        # items are stored as pointers to the classes (not instances)
        self._drawableClasses = collections.OrderedDict()
        self._drawableClasses.update({'MCHits' : mchit})
        # self._drawableClasses.update({'MCTracks' : mctrack})
        self._drawableClasses.update({'PMaps' : pmap})
        # self._drawableClasses.update({'Clusters' : cluster})
        # self._drawableClasses.update({'MCTracks' : mctrack})
        # self._drawableClasses.update({'sparse3d': sparse3d})
        # self._drawableClasses.update({'SiPM MCHits': sipmmchit})

    def getListOfTitles(self):
        return self._drawableClasses.keys()

    def getListOfItems(self):
        return zip(*self._drawableClasses.values())[1]

    def getDict(self):
        return self._drawableClasses


