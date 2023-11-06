import rasterio
from matplotlib import pyplot as plt
from rasterio.merge import merge
import rasterio.plot
import rasterio as rio
import io
import numpy as np

class GeoTiff:

    def fromCollection(paths):
        out = []
        for p in paths:
            out.append(GeoTiff(p))
        return merge(out)

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

        return GeoTiff("data/merge.tif")

    
    def __init__(self, path):
        self.tiff = rasterio.open(path)

    def to_numpy(self):
        return self.tiff.read()

    def visualize(self):
        rasterio.plot.show(self.tiff, title="GeoTIFF visualisation")
        return plt.gcf()

        
    def __str__(self):
        out = "GeoData with"
        out += f"\n Spacial bounding box:\n  Bottom-Left: {self.tiff.bounds.left, self.tiff.bounds.bottom}"
        out += f"\n  Top-Right: {self.tiff.bounds.right, self.tiff.bounds.top}"
        out += f"\n Number of Bands: {self.tiff.count}"
        out += f"\n Raster Size: {self.tiff.width, self.tiff.height}"
        out += f"\n Coordinate Reference: {self.tiff.crs}"
        return out