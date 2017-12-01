from invisible_cities.database import load_db
from invisible_cities.io import pmap_io, mchits_io

class io_manager(object):
    """docstring for io_manager"""
    def __init__(self):
        super(io_manager, self).__init__()
        
        # Load the database objects
        self._det_geo   = load_db.DetectorGeo()
        self._pmt_data  = load_db.DataPMT()
        self._sipm_data = load_db.DataSiPM()
        self._events = []
        self._entry = 0
        self._max_entry = 0
        self._run = 5

    def event(self):
        return self._events[self._entry]

    def entry(self):
        return self._entry

    def run(self):
        return self._run

    def set_file(self, _file_name):


        print("Got it: {}".format(_file_name))
        try:
            self._s1_dict, self._s2_dict, self._s2si_dict = pmap_io.load_pmaps(_file_name)
            self._has_pmaps = True
        except:
            self._has_pmaps = False

        try:
            self._mc_hits = mchits_io.load_mchits(_file_name)
            self._mc_part = mchits_io.load_mcparticles(_file_name)
            self._has_mc = True
        except:
            self._has_mc = False
            pass

        self._has_reco = False
        if not (self._has_reco or self._has_pmaps or self._has_mc):
            print("Couldn't load file {}.".format(_file_name))
            exit(-1)

        # Use the S2_dict as the list of events:
        self._events = list(self._s1_dict.keys())
        self._max_entry = len(self._events) -1

    def s1(self, event=-1):
        if event == -1:
            event = self._events[self._entry]
        if event not in self._events:
            print("Can't go to event {}".format(event))
        return self._s1_dict[event]

    def s2(self, event=-1):
        if event == -1:
            event = self._events[self._entry]
        if event not in self._events:
            print("Can't go to event {}".format(event))
        return self._s2_dict[event]

    def s2si(self, event=-1):
        if event == -1:
            event = self._events[self._entry]
        if event not in self._events:
            print("Can't go to event {}".format(event))
        return self._s2si_dict[event]

    def mchits(self, event=-1):
        if event == -1:
            event = self._events[self._entry]
        if event not in self._events:
            print("Can't go to event {}".format(event))
        return self._mc_hits[event]

    def mctracks(self, event=-1):
        if event == -1:
            event = self._events[self._entry]
        if event not in self._events:
            print("Can't go to event {}".format(event))
        return self._mc_part[event]        

    def det_geo(self):
        return self._det_geo

    def pmt_data(self):
        return self._pmt_data

    def sipm_data(self):
        return self._sipm_data

    def get_num_events(self):
        return len(self._events)

    def go_to_entry(self,entry):
        if entry >= 0 and entry < self.get_num_events():
            self._entry = entry
        else:
            print("Can't go to entry {}, entry is out of range.".format(entry))


