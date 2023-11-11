# Tests for the TiffFile class in geo_tiff.py
import GeoTIFFConverter as tiff

def tiff_consistency(data1, data2, data3, data4, compare):

    # Check that merged tile adheres to dimensions
    width = data1.tiff.width * 2
    height = data1.tiff.height * 2
    assert compare.tiff.width == width
    assert compare.tiff.height == height

    # Check that number of bands matches
    bands = data1.tiff.count
    assert compare.tiff.count == bands


def test_read_tiff():
    data = tiff.TiffFile("tests/1.tif") 


def test_tiff_merge():
    data1 = tiff.TiffFile("tests/1.tif")
    data2 = tiff.TiffFile("tests/2.tif")
    data3 = tiff.TiffFile("tests/3.tif")
    data4 = tiff.TiffFile("tests/4.tif")
    merged_data = tiff.TiffFile.merge([data1, data2, data3, data4])
    tiff_consistency(data1, data2, data3, data4, merged_data)

def test_tiff_from_collection():
    data1 = tiff.TiffFile("tests/1.tif")
    data2 = tiff.TiffFile("tests/2.tif")
    data3 = tiff.TiffFile("tests/3.tif")
    data4 = tiff.TiffFile("tests/4.tif")
    paths = ["tests/1.tif", "tests/2.tif", "tests/3.tif", "tests/4.tif"]
    merged_data = tiff.TiffFile.fromCollection(paths)
    tiff_consistency(data1, data2, data3, data4, merged_data)


