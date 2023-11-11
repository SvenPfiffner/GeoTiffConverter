from geopy.geocoders import Nominatim
import numpy as np

class Cartographer:
    """
    A class that provides static methods to perform various cartography tasks.
    """

    def coord_to_address(coord):
        """
        Retrieve the address of a given coordinate.

        Args:
        coord (Coordinate): A coordinate in the epsg:4326 projection

        Returns:
        str: The address at the given coordinate.
        """
        assert coord.proj_string == "epsg:4326", "Coordinate must be in latlong format"
        geolocator = Nominatim(user_agent="geo_tiff_converter")
        location = geolocator.reverse((coord.x, coord.y))
        return location.address
    
    def get_bbox_img(bbox):
        """
        Retrieve an aerial image of the area defined by a bounding box.

        Args:
        bbox (tuple): A tuple containing two instances of the Coordinate class that make up the bounding box.

        Returns:
        np.array: Aerial image of the specified area as an RGB numpy array.
        """
        coord1, coord2 = bbox
        assert coord1.proj_string == coord2.proj_string, "Coordinate projections don't match"
        assert coord1.proj_string == "epsg:4326", "Coordinates must be in latlong format"
        pass