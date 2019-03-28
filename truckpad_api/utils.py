from geopy.geocoders import Nominatim


def get_geolocation(city, state):
    location = Nominatim().geocode("{}, {}".format(city, state))
    return str(location.latitude), str(location.longitude)


def reverse_geolocation(latitude, longitude):
    location = Nominatim().reverse("{}, {}".format(latitude, longitude))
    return location.raw['address']['city'], location.raw['address']['state']
