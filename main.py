# Sandbox
import GeoTIFFConverter as tiff
import numpy as np

file1 = tiff.TiffFile("data/input/1.tif")

pcd = tiff.Solids.TiffPc.fromTiffFile(file1, downsample_voxel_size=10)
render_options = tiff.Solids.RenderOptions(show_coordinate_frame=False)
pcd.render(render_options)