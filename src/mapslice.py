import folium
from math import radians, cos, sin, sqrt, atan2

def haversine(lat, lon, distance_km):
    # Earth's radius in km
    R = 6371.0  
    
    # Approximate bounding box (assuming small area, ignoring curvature)
    d_lat = distance_km / R
    d_lon = distance_km / (R * cos(radians(lat)))
    
    # Top-right coordinates
    new_lat = lat + (d_lat * (180 / 3.14159))
    new_lon = lon + (d_lon * (180 / 3.14159))
    
    return new_lat, new_lon

def generate_map(bottom_left_lat, bottom_left_lon, distance_km):
    top_right_lat, top_right_lon = haversine(bottom_left_lat, bottom_left_lon, distance_km)

    # Center of map (approx midpoint)
    center_lat = (bottom_left_lat + top_right_lat) / 2
    center_lon = (bottom_left_lon + top_right_lon) / 2

    # Create a folium map
    map_slice = folium.Map(location=[center_lat, center_lon], zoom_start=12)

    # Draw a bounding box
    folium.Rectangle(
        bounds=[(bottom_left_lat, bottom_left_lon), (top_right_lat, top_right_lon)],
        color="blue",
        fill=True,
        fill_opacity=0.2
    ).add_to(map_slice)

    # Save map to file
    map_slice.save("map_slice.html")
    print("Map saved as 'map_slice.html'. Open it in a browser.")

if __name__ == "__main__":
    lat = float(input("Enter bottom-left latitude: "))
    lon = float(input("Enter bottom-left longitude: "))
    distance_km = float(input("Enter distance (km): "))

    generate_map(lat, lon, distance_km)
