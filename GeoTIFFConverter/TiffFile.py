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

    def fromCollection(paths):
        out = []
        for p in paths:
            out.append(TiffFile(p))
        return TiffFile.merge(out)

    def merge(geoTiffs):
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
        self.tiff = rasterio.open(path)

    def to_numpy(self):
        return self.tiff.read()

    def visualize(self):
        rasterio.plot.show(self.tiff, title="GeoTIFF visualisation")
        return plt.gcf()
    
    def get_bounding_coordinates(self):
        x1, y1 = self.tiff.bounds.left, self.tiff.bounds.bottom
        x2, y2 = self.tiff.bounds.right, self.tiff.bounds.top
        return Coordinate((x1, y1), self.get_proj()), Coordinate((x2, y2), self.get_proj())
    
    def get_proj(self):
        return self.tiff.crs

    def __str__(self):
        bbox = self.get_bounding_coordinates()
        out = "GeoData with"
        out += f"\n Spacial bounding box:\n  Bottom-Left: {bbox[0]}"
        out += f"\n  Top-Right: {bbox[1]}"
        out += f"\n Number of Bands: {self.tiff.count}"
        out += f"\n Raster Size: {self.tiff.width, self.tiff.height}"
        out += f"\n Coordinate Reference: {self.get_proj()}"
        return out