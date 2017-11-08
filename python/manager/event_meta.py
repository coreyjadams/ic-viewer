
class event_meta3D(object):
    def __init__(self):
        super(event_meta3D, self).__init__()

    def refresh(self):

        self._x_min   = 0.0
        self._y_min   = 0.0
        self._z_min   = 0.0
        self._x_max   = 480.
        self._y_max   = 480.
        self._z_max   = 600.
        self._y_n_pixels = 48.
        self._x_n_pixels = 48.
        self._z_n_pixels = 60.
        self._size_voxel_x = 10
        self._size_voxel_y = 10
        self._size_voxel_z = 10


    def size_voxel_x(self):
        return self._size_voxel_x

    def size_voxel_y(self):
        return self._size_voxel_y

    def size_voxel_z(self):
        return self._size_voxel_z

    def n_voxels_x(self):
        return self._x_n_pixels

    def n_voxels_y(self):
        return self._y_n_pixels

    def n_voxels_z(self):
        return self._y_n_pixels

    def dim_x(self):
        return self._x_max

    def dim_y(self):
        return self._y_max

    def dim_z(self):
        return self._z_max

    def width(self):
        return self.dim_x()

    def height(self):
        return self.dim_y()

    def length(self):
        return self.dim_z()

    def min_y(self):
        return self._y_min

    def max_y(self):
        return self._y_max

    def min_x(self):
        return self._x_min

    def max_x(self):
        return self._x_max

    def min_z(self):
        return self._z_min    

    def max_z(self):
        return self._z_max
