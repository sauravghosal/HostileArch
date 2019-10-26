import requests
import googlemaps
from datetime import datetime


def reverseGeocode():
    # URL = "http://maps.googleapis.com/maps/api/geocode/json"

    # # location given here
    # location = "delhi technological university"

    # # defining a params dict for the parameters to be sent to the API
    # PARAMS = {'address':location}

    # # sending get request and saving the response as response object
    # r = requests.get(url = URL, params = PARAMS)

    # # extracting data in json format
    # data = r.json()

    # print(data)

    # # extracting latitude, longitude and formatted address
    # # of the first matching location
    # latitude = data['results'][0]['geometry']['location']['lat']
    # longitude = data['results'][0]['geometry']['location']['lng']
    # formatted_address = data['results'][0]['formatted_address']

    # # printing the output
    # print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"
    #       %(latitude, longitude,formatted_address))
    gmaps = googlemaps.Client(key="AIzaSyACXhXaxtZ3mw7-2d2vjIckekoE4lQbY48")

    # Geocoding an address
    geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

    # Look up an address with reverse geocoding
    reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

    # Request directions via public transit
    now = datetime.now()
    directions_result = gmaps.directions("Sydney Town Hall",
                                         "Parramatta, NSW",
                                         mode="transit",
                                         departure_time=now)

def main():
    reverseGeocode()

if __name__ == "__main__": main()
