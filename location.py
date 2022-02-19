import requests
from geopy.geocoders import Nominatim
import geocoder
import pandas as pd
import folium
import geopy.distance
import numpy as np


def get_user_location():
    r = requests.get("https://get.geojs.io")
    ip_request = requests.get("https://get.geojs.io/v1/ip.json")
    ip_add = ip_request.json()['ip']
    url = f'https://get.geojs.io/v1/ip/geo/{ip_add}.json'
    geo_request = requests.get(url)
    geo_data = geo_request.json()
    return float(geo_data['latitude']), float(geo_data['longitude']), ip_add


# user_location = get_user_location_and_ip()


def get_users_address(user_location):
    locator = Nominatim(user_agent="MyGeocoder")
    location = locator.reverse(user_location)
    return location.address


# location = get_users_address(user_location)

def nearest_police_stations(user_location):
    police_data = pd.read_csv("PoliceLocations.csv")
    police_data.head()
    police_data['Lat'] = police_data.Cordinates.str.split(",", expand=True)[0]
    police_data['Long'] = police_data.Cordinates.str.split(",", expand=True)[1]
    police_data.Lat = police_data.Lat.str.split("(", expand=True)[1].astype(float)
    police_data.Long = police_data.Long.str.split(")", expand=True)[0].astype(float)
    cords = []
    for lat, lng in zip(police_data.Lat, police_data.Long):
        cords.append(tuple([lat, lng]))
    police_data['new'] = cords
    distances = []
    for stations in police_data.new:
        distances.append(geopy.distance.distance(user_location, stations).km)
    return distances, police_data


def map_plotting(user_location, distances, police_data):
    nearest = np.argsort(distances)[:3]
    m = folium.Map(location=user_location, zoom_start=12)
    for i in range(3):
        folium.Marker(location=police_data.new[nearest[i]], icon=folium.Icon(color='red')).add_to(m)
    folium.Marker(location=user_location, icon=folium.Icon(color='blue')).add_to(m)
    return m, np.array(distances)[nearest], police_data.Name[nearest[0]]
