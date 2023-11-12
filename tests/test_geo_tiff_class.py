# Tests for the TiffFile class in geo_tiff.py
import GeoTIFFConverter as tiff

def test_read_tiff():
    data = tiff.TiffFile("tests/1.tif") 


def test_tiff_from_collection():
    data1 = tiff.TiffFile("tests/1.tif")
    data2 = tiff.TiffFile("tests/2.tif")
    data3 = tiff.TiffFile("tests/3.tif")
    data4 = tiff.TiffFile("tests/4.tif")
    paths = ["tests/1.tif", "tests/2.tif", "tests/3.tif", "tests/4.tif"]
    merged_data = tiff.TiffFile.fromCollection(paths)


