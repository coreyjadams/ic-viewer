from pyqtgraph.Qt import QtCore
from .event_meta import NEW_meta
from .io_manager import io_manager

class evd_manager_base(QtCore.QObject):

    eventChanged = QtCore.pyqtSignal()
    metaRefreshed = QtCore.pyqtSignal(NEW_meta)

    """docstring for lariat_manager"""

    def __init__(self, config, _file=None):
        super(evd_manager_base, self).__init__()
        QtCore.QObject.__init__(self)
        # self.init_manager(_file)

    def init_manager(self, _file):


        self._io_manager = io_manager()
        self._io_manager.set_file(_file)

        self.go_to_entry(0)

        # # Meta keeps track of information about number of planes, visible
        # # regions, etc.:
        self._meta = NEW_meta()


        # Drawn classes is a list of things getting drawn, as well.
        self._drawnClasses = dict()

        self._keyTable = dict()


    def meta(self):
        return self._meta


    # This function returns the list of products that can be drawn:
    def getDrawableProducts(self):
        return self._drawableItems.getDict()

    # def internalEvent(self):
    def entry(self):
        return self._io_manager.entry()

    def run(self):
        return self._io_manager.run()

    def event(self):
        return 0

    def n_entries(self):
        if self._io_manager is not None:
            return self._io_manager.get_num_events()
        else:
            return 0

    # def n_runs(self):
    #     if self._io_manager is not None:
    #         return self._io_manager.getNumRunsFile()
    #     else:
    #         return 0

    # override the functions from manager as needed here
    def next(self):
        if self.entry() + 1 < self.n_entries():
            self.go_to_entry(self.entry() + 1)
        else:
            print("On the last event, can't go to next.")

    def prev(self):
        if self.entry != 0:
            self.go_to_entry(self.entry() - 1)
        else:
            print("On the first event, can't go to previous.")

    def go_to_entry(self, entry):
        self._io_manager.go_to_entry(entry)
        self.eventChanged.emit()
