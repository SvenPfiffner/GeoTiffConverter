# Tests for the GeoTiff class in geo_tiff.py
import GeoTIFFConverter as tiff

def tiff_consistency(data1, data2, data3, data4, compare):

    # Check that merged tile adheres to dimensions
    width = data1.tiff.width + data2.tiff.width + data3.tiff.width + data4.tiff.width
    height = data1.tiff.height + data2.tiff.height + data3.tiff.height + data4.tiff.height
    assert compare.tiff.width == width
    assert compare.tiff.height == height

    # Check that number of bands matches
    bands = data1.tiff.count
    assert compare.tiff.count == bands


def test_read_tiff():
    data = tiff.GeoTiff("1.tif") 


def test_tiff_merge():
    data1 = tiff.GeoTiff("1.tif")
    data2 = tiff.GeoTiff("2.tif")
    data3 = tiff.GeoTiff("3.tif")
    data4 = tiff.GeoTiff("4.tif")
    merged_data = tiff.GeoTiff.merge([data1, data2, data3, data4])
    tiff_consistency(data1, data2, data3, data4, merged_data)

def test_tiff_from_collection():
    data1 = tiff.GeoTiff("1.tif")
    data2 = tiff.GeoTiff("2.tif")
    data3 = tiff.GeoTiff("3.tif")
    data4 = tiff.GeoTiff("4.tif")
    paths = ["1.tif", "2.tif", "3.tif", "4.tif"]
    merged_data = tiff.GeoTiff.fromCollection(paths)
    tiff_consistency(data1, data2, data3, data4, merged_data)


