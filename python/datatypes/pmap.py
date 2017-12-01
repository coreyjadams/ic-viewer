from .database import recoBase3D
from pyqtgraph.Qt import QtGui, QtCore
import numpy
try:
    import pyqtgraph.opengl as gl
except:
    print("Error, must have open gl to use this viewer.")
    exit(-1)

class pmap(recoBase3D):

    """docstring for pmap"""

    def __init__(self):
        super(pmap, self).__init__()
        self._product_name = 'pmap'
        self._gl_voxel_mesh = None
        self._x = None
        self._y = None
        self._z = None
        self._vals = None
        self._meta = None

        self._box_template = numpy.array([[ 0 , 0, 0],
                                          [ 1 , 0, 0],
                                          [ 1 , 1, 0],
                                          [ 0 , 1, 0],
                                          [ 0 , 0, 1],
                                          [ 1 , 0, 1],
                                          [ 1 , 1, 1],
                                          [ 0 , 1, 1]],
                                         dtype=float)


        self._faces_template = numpy.array([[0, 1, 2],
                                            [0, 2, 3],
                                            [0, 1, 4],
                                            [1, 5, 4],
                                            [1, 2, 5],
                                            [2, 5, 6],
                                            [2, 3, 6],
                                            [3, 6, 7],
                                            [0, 3, 7],
                                            [0, 4, 7],
                                            [4, 5, 7],
                                            [5, 6, 7]])

    # this is the function that actually draws the cluster.
    def drawObjects(self, view_manager, io, meta):

        # Get the data from the file:
        # print (io.s2si())

        self._meta = meta
        # Loop over the s2si pmap and fill the voxels
        # Z position has to be calculated based on the difference in time between s1 ands s2

        t0 = 1e-3*io.s1().peaks[0].tpeak


        self._x = []
        self._y = []
        self._z = []
        self._vals = []

        i = 0
        for i_peak in range(io.s2si().number_of_peaks):
            for sipm in io.s2si().sipms_in_peak(i_peak):
                wfm = io.s2si().sipm_waveform(i_peak,sipm)
                # Fill the variables as needed:
                for t, e in zip(wfm.t, wfm.E):
                    if e != 0:
                        self._x.append(io.sipm_data().X[sipm])
                        self._y.append(io.sipm_data().Y[sipm])
                        self._z.append((1e-3*t - t0))
                        # print(t)
                        # print(t0)
                        # print (t0 - t)
                        self._vals.append(e)

            # self._points[i][0] = _mc_hits[i].GetPosition().x()
            # self._points[i][1] = _mc_hits[i].GetPosition().y()
            # self._points[i][2] = _mc_hits[i].GetPosition().z()
            # self._vals[i] = _mc_hits[i].GetAmplitude()

            i += 1

        self._min_coords = numpy.asarray((numpy.min(self._x), 
                                         numpy.min(self._y), 
                                         numpy.min(self._z)))
        self._max_coords = numpy.asarray((numpy.max(self._x), 
                                         numpy.max(self._y), 
                                         numpy.max(self._z)))

        self.redraw(view_manager)


    def redraw(self, view_manager):

        if self._gl_voxel_mesh is not None:
            view_manager.getView().removeItem(self._gl_voxel_mesh)
            self._gl_voxel_mesh = None


        verts, faces, colors = self.buildTriangleArray(view_manager)


        #make a mesh item: 
        mesh = gl.GLMeshItem(vertexes=verts,
                             faces=faces,
                             faceColors=colors,
                             smooth=False)

        mesh.setGLOptions("translucent")        
        self._gl_voxel_mesh = mesh
        view_manager.getView().addItem(self._gl_voxel_mesh)


    def buildTriangleArray(self, view_manager):
        verts = None
        faces = None
        colors = None


        i = 0
        for x, y, z, val in zip(self._x, self._y, self._z, self._vals):

            # Don't draw this pixel if it's below the threshold:
            if val < view_manager.getLevels()[0]:
                continue


            this_color = self.getColor(view_manager.getLookupTable(),
                                       view_manager.getLevels(),
                                       val)

            if colors is None:
                colors = numpy.asarray([this_color]*12)
            else:
                colors = numpy.append(colors,
                                      numpy.asarray([this_color]*12),
                                      axis=0)

            # print "({}, {}, {})".format(_pos[0], _pos[1], _pos[2])
            this_verts = self.makeBox(x, y, z, self._meta)

            if faces is None:
                faces = self._faces_template
            else:
                faces = numpy.append(faces, 
                                     self._faces_template + 8*i, 
                                     axis=0)
            if verts is None:
                verts = this_verts
            else:
                verts = numpy.append(verts, 
                                     this_verts, axis=0)

            i += 1

        return verts, faces, colors

    def makeBox(self, x, y, z , meta):
        verts_box = numpy.copy(self._box_template)
        #Scale all the points of the box to the right voxel size:
        verts_box[:,0] *= meta.size_voxel_x()
        verts_box[:,1] *= meta.size_voxel_y()
        verts_box[:,2] *= meta.size_voxel_z()

        #Shift the points to put the center of the cube at (0,0,0)
        verts_box[:,0] -= 0.5*meta.size_voxel_x()
        verts_box[:,1] -= 0.5*meta.size_voxel_y()
        verts_box[:,2] -= 0.5*meta.size_voxel_z()
        
        #Move the points to the right coordinate in this space

        verts_box[:,0] += x
        verts_box[:,1] += y
        verts_box[:,2] += z


        # color_arr = numpy.ndarray((12, 4))
        # color_arr[:] = [1,1,1,1]

        return verts_box


    def getColor(self, _lookupTable, _levels, _voxel_value ):
        _min = _levels[0]
        _max = _levels[1]

        if _voxel_value >= _max:
            # print "Max " + str(_voxel_value)
            return _lookupTable[-1]
        elif _voxel_value < _min:
            # print "Min "  + str(_voxel_value)
            return (0,0,0,0)
        else:
            index = 255*(_voxel_value - _min) / (_max - _min)
            return _lookupTable[int(index)]


    def clearDrawnObjects(self, view_manager):
        if self._gl_voxel_mesh is not None:
            view_manager.getView().removeItem(self._gl_voxel_mesh)

        self._gl_voxel_mesh = None
        self._points = None
        self._vals = None
        self._colors = None
        self._x = []
        self._y = []
        self._z = []
        self._vals = []

    def refresh(self, view_manager):
        self.redraw(view_manager)