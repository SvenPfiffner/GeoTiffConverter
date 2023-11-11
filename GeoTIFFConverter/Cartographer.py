# Author: Sven Pfiffner
# Created: November 2023

from geopy.geocoders import Nominatim
import numpy as np
from owslib.wms import WebMapService
from io import BytesIO
from PIL import Image

class Cartographer:
    """
    A class that provides static methods to perform various cartography tasks.
    """

    @staticmethod
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
    
    @staticmethod
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

        # Connect to GIBS WMS Service
        wms = WebMapService('https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?', version='1.1.1')

        # Configure request for BlueMarble_NextGeneration
        resp = wms.getmap(layers=['BlueMarble_NextGeneration'],  # Layers
                 srs="epsg:4326",  # Map projection
                 bbox=(coord1.x, coord1.y, coord2.x, coord2.y),  # Bounds
                 size=(1200, 600),  # Image size
                 time='2021-09-21',  # Time of data
                 format='image/png',  # Image format
                 transparent=True)  # Nodata transparency
        
        img = Image.open(BytesIO(resp.read()))

        return np.array(img)