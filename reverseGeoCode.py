import requests
import googlemaps
from datetime import datetime


def reverseGeocode(coordinates):
    gmaps = googlemaps.Client(key="AIzaSyACXhXaxtZ3mw7-2d2vjIckekoE4lQbY48")

    # Look up an address with reverse geocoding
    result = gmaps.reverse_geocode(coordinates)
    ans = result[0]["formatted_address"]
    print(ans)

def main():
    reverseGeocode((40.714224, -73.961452))

if __name__ == "__main__": main()
