import googlemaps
import streamlit as st

def get_googlemaps_client():
    """
    Initializes and returns the Google Maps client using the API key from st.secrets.
    """
    try:
        api_key = st.secrets["GOOGLE_MAPS_API_KEY"]
        return googlemaps.Client(key=api_key)
    except Exception as e:
        print(f"Error initializing Google Maps Client: {e}")
        return None

def calculate_route_distance(origin_place, dest_place):
    """
    Calculates driving distance in kilometers between two places (can be cities, farms, businesses)
    using the official Google Maps Directions API.
    """
    if not origin_place or not dest_place:
        return None

    gmaps = get_googlemaps_client()
    if not gmaps:
        return None

    try:
        # Request directions via driving
        directions_result = gmaps.directions(origin_place, dest_place, mode="driving")

        if directions_result and len(directions_result) > 0:
            # Distance is in meters, extract it from the first leg of the first route
            distance_meters = directions_result[0]['legs'][0]['distance']['value']
            return distance_meters / 1000.0
        else:
            print("Google Maps returned no routes.")
            return None
    except Exception as e:
        print(f"Error fetching route from Google Maps: {e}")
        return None
