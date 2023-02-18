import folium
from scapy.layers.inet import traceroute
import socket
import geocoder
import webbrowser
import pandas as pd
import requests
from geopy.geocoders import Nominatim

ipList = []
locationList = []
g = geocoder.ip('me')
geolocator = Nominatim(user_agent="geoapiExercises")


def main(link):
    addr = socket.gethostbyname(str(link))
    target = [addr]
    result, unans = traceroute(target, maxttl=10)

    for item in result.get_trace()[list(result.get_trace())[0]].keys():
        ipList.append(result.get_trace()[list(result.get_trace())[0]][item][0])

    for ip in ipList:
        locationLat = (requests.get(f"https://geolocation-db.com/json/{ip}&position=true").json())['latitude']
        locationLong = (requests.get(f"https://geolocation-db.com/json/{ip}&position=true").json())['longitude']
        locationList.append((locationLat, locationLong))

    class Map:
        def __init__(self, center, zoom_start):
            self.center = center
            self.zoom_start = zoom_start

        def showMap(self):
            # Create the map
            my_map = folium.Map(location=self.center, zoom_start=self.zoom_start)
            lat = []
            long = []
            name = []
            for i in range(len(locationList)):
                lat.append(locationList[i][0])
                long.append(locationList[i][1])

            lat.pop(0)
            long.pop(0)

            for i in range(len(locationList) - 1):
                name.append(geolocator.reverse(str(lat[i]) + "," + str(long[i])))

            data = pd.DataFrame({
                'lon': long,
                'lat': lat,
                'name': name
            }, dtype=object)

            for i in range(0, len(data)):
                folium.Marker(
                    location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
                    popup=data.iloc[i]['name'],
                ).add_to(my_map)

            # Display the map
            my_map.save("templates/map.html")

    # Define coordinates of where we want to center our map
    coords = g.latlng
    m = Map(center=coords, zoom_start=15)
