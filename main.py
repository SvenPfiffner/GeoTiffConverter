# Sandbox
import GeoTIFFConverter as tiff

file1 = tiff.TiffFile("data/input/1.tif")

mesh = tiff.Solids.TiffMesh(file1)