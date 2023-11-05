import GeoTIFFConverter as tiff

file1 = tiff.GeoTiff("data/input/1.tif")


print(tiff.Converter.to_point_cloud(file1)[0])