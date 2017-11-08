import h5py
import tables
from ROOT import gate
from pyqtgraph.Qt import QtCore
from event_meta import event_meta3D

class evd_manager_base(QtCore.QObject):

    eventChanged = QtCore.pyqtSignal()
    drawFreshRequested = QtCore.pyqtSignal()
    metaRefreshed = QtCore.pyqtSignal(event_meta3D)

    """docstring for lariat_manager"""

    def __init__(self, config, _file=None):
        super(evd_manager_base, self).__init__()
        QtCore.QObject.__init__(self)
        # self.init_manager(_file)

    def init_manager(self, _file):

        self._entry = 0

        self._io_manager = gate.Centella.instance(gate.MUTE)
        self._io_manager.addInputFile(_file)
        self._io_manager.initialize()

        self._entry = 0
        self._run = 0

        self._Run = None
        self._Event = None

        self.go_to_entry(0)

        # # Meta keeps track of information about number of planes, visible
        # # regions, etc.:
        self._meta = event_meta3D()


        # Drawn classes is a list of things getting drawn, as well.
        self._drawnClasses = dict()

        self._keyTable = dict()

        self._meta.refresh()

    def meta(self):
        return self._meta


    # This function returns the list of products that can be drawn:
    def getDrawableProducts(self):
        return self._drawableItems.getDict()

    # def internalEvent(self):
    def entry(self):
        return self._entry

    def run(self):
        return self._run

    def event(self):
        return self._Event.GetEventID()

    def n_entries(self):
        if self._io_manager is not None:
            return self._io_manager.getNumEventsFile()
        else:
            return 0

    def n_runs(self):
        if self._io_manager is not None:
            return self._io_manager.getNumRunsFile()
        else:
            return 0

    # override the functions from manager as needed here
    def next(self):
        if self.entry() + 1 < self.n_entries():
            # print self._driver.event()
            self.go_to_entry(self._entry + 1)
        else:
            print "On the last event, can't go to next."

    def prev(self):
        if self.entry != 0:
            self.go_to_entry(self._entry - 1)
        else:
            print "On the first event, can't go to previous."

    def go_to_entry(self, entry):
        if entry >= 0 and entry < self.n_entries():
            self._entry = entry
            self._Event = self._io_manager.read(self._entry)
            if self._Run is None or self._io_manager.isNewFile():
                self._Run = self._io_manager.read_irun_info(self._run)

            # Temporary, listing available things:
            # print "GetEnergy size: {}".format(self._Event.GetEnergy().size())
            print "GetHits size: {}".format(self._Event.GetHits().size())
            print "GetHitMaps size: {}".format(self._Event.GetHitMaps().size())
            print "GetClusters size: {}".format(self._Event.GetClusters().size())
            print "GetTracks size: {}".format(self._Event.GetTracks().size())
            print "GetSignals size: {}".format(self._Event.GetSignals().size())
            print "GetParticles size: {}".format(self._Event.GetParticles().size())
            print "GetMCHits size: {}".format(self._Event.GetMCHits().size())
            print "GetMCSensHits size: {}".format(self._Event.GetMCSensHits().size())
            print "GetMCTracks size: {}".format(self._Event.GetMCTracks().size())
            print "GetMCParticles size: {}".format(self._Event.GetMCParticles().size())
            print
            self.eventChanged.emit()
        else:
            print "Can't go to entry {}, entry is out of range.".format(entry)
