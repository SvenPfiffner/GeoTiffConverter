# Author: Sven Pfiffner
# Created: November 2023

import rasterio
from matplotlib import pyplot as plt
from rasterio.merge import merge
import rasterio.plot
import rasterio as rio
import io
import numpy as np
import math
import pyproj
from .Coordinate import Coordinate

class TiffFile:
    """
    A class for handling GeoTIFF files and performing various operations on them.
    """

    def fromCollection(paths):
        """
        Create a TiffFile instance from a collection of file paths.

        Args:
        paths (list): A list of file paths to GeoTIFF files.

        Returns:
        TiffFile: A merged TiffFile from the collection of TiffFiles.
        """

        out = []
        for p in paths:
            out.append(TiffFile(p))
        return TiffFile.merge(out)

    def merge(geoTiffs):
        """
        Merge multiple GeoTIFFs into a single file.

        Args:
        geoTiffs (list): A list of TiffFile instances to be merged.

        Returns:
        TiffFile: A TiffFile instance representing the merged GeoTIFF.
        """

        rasters = []
        for g in geoTiffs:
            rasters.append(g.tiff)

        mosaic, output = merge(rasters)
        output_meta = rasters[0].meta.copy()
        output_meta.update(
            {"driver": "GTiff",
                "height": mosaic.shape[1],
                "width": mosaic.shape[2],
                "transform": output,
            }
        )
        with rio.open("data/merge.tif", "w", **output_meta) as m:
            m.write(mosaic)

        return TiffFile("data/merge.tif")

    
    def __init__(self, path):
        """
        Initialize a TiffFile instance from a file path.

        Args:
        path (str): Path to the GeoTIFF file.
        """

        self.tiff = rasterio.open(path)

    def to_numpy(self):
        """
        Read the GeoTIFF data as a NumPy array.

        Returns:
        np.array: A NumPy array containing the GeoTIFF data.
        """

        return self.tiff.read()

    def visualize(self):
        """
        Visualize the GeoTIFF using Matplotlib.

        Returns:
        plt.figure: The Matplotlib figure object showing the GeoTIFF.
        """

        rasterio.plot.show(self.tiff, title="GeoTIFF visualisation")
        return plt.gcf()
    
    def get_bounding_coordinates(self, target_format=""):
        """
        Retrieve the bounding coordinates of the GeoTIFF.

        Args:
        target_format (str, optional): The target projection of the bounding coordinates. If none is
        given, the projection stored in the TIFF file is used. Defaults to "".

        Returns:
        tuple: A tuple containing Coordinate instances for the bounding box.
        """

        x1, y1 = self.tiff.bounds.left, self.tiff.bounds.bottom
        x2, y2 = self.tiff.bounds.right, self.tiff.bounds.top
        bbox = Coordinate((x1, y1), self.get_proj()), Coordinate((x2, y2), self.get_proj())
        if format != "":
            bbox = bbox[0].convert(format), bbox[1].convert(format)
        return bbox

    def get_proj(self):
        """
        Get the coordinate reference system of the GeoTIFF.

        Returns:
        CRS: The coordinate reference system of the GeoTIFF.
        """

        return self.tiff.crs

    def __str__(self):
        """
        Generate a string representation of the TiffFile instance.

        Returns:
        str: A string summarizing the TiffFile instance details.
        """
        
        bbox = self.get_bounding_coordinates()
        out = "GeoData with"
        out += f"\n Spacial bounding box:\n  Bottom-Left: {bbox[0]}"
        out += f"\n  Top-Right: {bbox[1]}"
        out += f"\n Number of Bands: {self.tiff.count}"
        out += f"\n Raster Size: {self.tiff.width, self.tiff.height}"
        out += f"\n Coordinate Reference: {self.get_proj()}"
        return out