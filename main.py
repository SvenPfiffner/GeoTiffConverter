# Sandbox
import GeoTIFFConverter as tiff

file1 = tiff.TiffFile("data/input/1.tif")

bbox = file1.get_bounding_coordinates("epsg:4326")

aerial_img = tiff.Cartographer.get_bbox_img(bbox)