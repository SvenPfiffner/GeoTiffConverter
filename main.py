# Sandbox
import GeoTIFFConverter as tiff

file1 = tiff.GeoTiff("data/input/1.tif")
file2 = tiff.GeoTiff("data/input/2.tif")


tiff.Converter.to_point_cloud([file1, file2])