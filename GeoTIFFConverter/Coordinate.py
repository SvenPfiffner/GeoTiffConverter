import pyproj
import numpy as np

class Coordinate:

    def __init__(self, coord_elems, proj_string):
        self.coord_elems = coord_elems
        self.proj_string = proj_string
        self.x = coord_elems[0]
        self.y = coord_elems[1]

    def convert(self, target_proj_string):
        if self.proj_string == target_proj_string:
            # The system is already in target projection, no conversion necessary
            return self.coord_elems
        
        # Perform conversion with pyproj
        print(self.proj_string)
        source_proj = pyproj.Proj(init=self.proj_string)
        target_proj = pyproj.Proj(init=target_proj_string)
        y, x = pyproj.transform(source_proj, target_proj, self.x, self.y)

        return Coordinate((x,y), target_proj_string)
    
    def as_latlong(self):
        return self.convert("epsg:4326")
    
    def to_numpy(self):
        return np.array([[self.x], [self.y]])
    
    def get_midpoint(coord1, coord2):
        assert coord1.proj_string == coord2.proj_string, "Projections don't match"
        x, y = (coord1.x + coord2.x) / 2, (coord1.y + coord2.y) / 2
        return Coordinate((x,y), coord1.proj_string)
