from geopy.geocoders import Nominatim

class Cartographer:

    def coord_to_address(coord):
        assert coord.proj_string == "epsg:4326", "Coordinate must be in latlong format"
        geolocator = Nominatim(user_agent="geo_tiff_converter")
        location = geolocator.reverse((coord.x, coord.y))
        return location.address