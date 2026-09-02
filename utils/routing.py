import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

def get_coordinates(city_name):
    """
    Returns (latitude, longitude) for a given city name using Nominatim (OpenStreetMap).
    """
    if not city_name or not city_name.strip():
        return None

    # Standard user_agent to avoid getting blocked
    geolocator = Nominatim(user_agent="freight_calculator_app")

    try:
        # Add 'Brazil' to the query to restrict results, assuming operations are primarily in Brazil
        location = geolocator.geocode(f"{city_name}, Brazil", timeout=10)
        if location:
            return location.latitude, location.longitude
        return None
    except GeocoderTimedOut:
        return None
    except Exception as e:
        print(f"Error geocoding {city_name}: {e}")
        return None

def get_driving_distance(coords1, coords2):
    """
    Calculates driving distance in kilometers between two coordinates (lat, lon)
    using the public OSRM API.
    """
    if not coords1 or not coords2:
        return None

    lat1, lon1 = coords1
    lat2, lon2 = coords2

    # OSRM expects coordinates in lon,lat format
    url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "Ok" and "routes" in data and len(data["routes"]) > 0:
                # distance is returned in meters
                distance_meters = data["routes"][0]["distance"]
                return distance_meters / 1000.0
        return None
    except Exception as e:
        print(f"Error fetching route from OSRM: {e}")
        return None

def calculate_route_distance(origin_city, dest_city):
    """
    Wrapper function to get driving distance directly from city names.
    Returns distance in km, or None if it fails.
    """
    origin_coords = get_coordinates(origin_city)
    dest_coords = get_coordinates(dest_city)

    if origin_coords and dest_coords:
        # Avoid spamming APIs
        time.sleep(1)
        return get_driving_distance(origin_coords, dest_coords)
    return None
