# Author: Sven Pfiffner
# Created: November 2023

import pyproj
import numpy as np

class Coordinate:
    """
    A class representing geographic coordinates with projection information.
    """

    def __init__(self, coord_elems, proj_string):
        """
        Initialize a Coordinate object.

        Args:
        coord_elems (tuple): The coordinate elements (x, y).
        proj_string (str): The projection string (e.g., 'epsg:4326').
        """

        self.coord_elems = coord_elems
        self.proj_string = proj_string
        self.x = coord_elems[0]
        self.y = coord_elems[1]

    def convert(self, target_proj_string):
        """
        Convert the coordinate to a different projection.

        Args:
        target_proj_string (str): The target projection string.

        Returns:
        Coordinate: The converted coordinate in the target projection.
        """

        if self.proj_string == target_proj_string:
            # The system is already in target projection, no conversion necessary
            return self.coord_elems
        
        # Perform conversion with pyproj
        transformer = pyproj.Transformer.from_crs(self.proj_string, target_proj_string)
        x, y = transformer.transform(self.x, self.y)

        return Coordinate((x,y), target_proj_string)
    
    def as_latlong(self):
        """
        Convert the coordinate to the 'epsg:4326' (lat-long) projection.

        Returns:
        Coordinate: The coordinate in 'epsg:4326' projection.
        """

        return self.convert("epsg:4326")
    
    def to_numpy(self):
        """
        Convert the coordinate to a NumPy array.

        Returns:
        np.array: A NumPy column vector containing the coordinate elements.
        """

        return np.array([[self.x], [self.y]])
    
    def get_midpoint(coord1, coord2):
        """
        Calculate the midpoint between two coordinates.

        Args:
        coord1 (Coordinate): The first coordinate.
        coord2 (Coordinate): The second coordinate.

        Returns:
        Coordinate: The midpoint coordinate between coord1 and coord2.
        """
        
        assert coord1.proj_string == coord2.proj_string, "Projections don't match"
        x, y = (coord1.x + coord2.x) / 2, (coord1.y + coord2.y) / 2
        return Coordinate((x,y), coord1.proj_string)
