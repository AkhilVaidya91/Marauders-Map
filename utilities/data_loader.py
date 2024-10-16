import requests
import pandas as pd
import re
import math
from typing import Tuple, List, Dict

def fetch_osm_data(lat: float, lon: float, radius: int) -> List[Dict]:
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
      node["name"](around:{radius},{lat},{lon});
      way["name"](around:{radius},{lat},{lon});
      relation["name"](around:{radius},{lat},{lon});
    );
    out center;
    """
    
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()
    return data['elements']

def determine_location_type(tags: Dict[str, str]) -> str:
    # Residential
    if 'building' in tags and tags['building'] in ['residential', 'house', 'apartments', 'detached', 'terrace', 'dormitory', 'bungalow']:
        return 'Residential'
    
    # Commercial
    if any(key in tags for key in ['shop', 'office', 'craft']):
        return 'Commercial'
    if 'building' in tags and tags['building'] in ['commercial', 'office', 'retail', 'supermarket', 'kiosk']:
        return 'Commercial'
    
    # Industrial
    if 'building' in tags and tags['building'] in ['industrial', 'warehouse', 'factory', 'manufacture']:
        return 'Industrial'
    if 'industrial' in tags or 'industry' in tags:
        return 'Industrial'
    
    # Educational
    if 'amenity' in tags and tags['amenity'] in ['school', 'university', 'college', 'library', 'kindergarten', 'language_school']:
        return 'Educational'
    
    # Healthcare
    if 'amenity' in tags and tags['amenity'] in ['hospital', 'clinic', 'doctors', 'dentist', 'pharmacy', 'veterinary']:
        return 'Healthcare'
    
    # Food & Drink
    if 'amenity' in tags and tags['amenity'] in ['restaurant', 'cafe', 'bar', 'fast_food', 'pub', 'food_court']:
        return 'Food & Drink'
    
    # Leisure & Entertainment
    if 'leisure' in tags or 'tourism' in tags:
        return 'Leisure & Entertainment'
    if 'amenity' in tags and tags['amenity'] in ['theatre', 'cinema', 'nightclub', 'arts_centre', 'community_centre']:
        return 'Leisure & Entertainment'
    
    # Transportation
    if 'amenity' in tags and tags['amenity'] in ['parking', 'bicycle_parking', 'bus_station', 'ferry_terminal']:
        return 'Transportation'
    if 'highway' in tags or 'railway' in tags or 'aeroway' in tags:
        return 'Transportation'
    
    # Religious
    if 'amenity' in tags and tags['amenity'] in ['place_of_worship', 'monastery']:
        return 'Religious'
    
    # Government & Public Services
    if 'amenity' in tags and tags['amenity'] in ['townhall', 'courthouse', 'police', 'fire_station', 'post_office']:
        return 'Government & Public Services'
    
    # Parks & Recreation
    if 'leisure' in tags and tags['leisure'] in ['park', 'playground', 'sports_centre', 'stadium', 'garden']:
        return 'Parks & Recreation'
    
    # Natural
    if 'natural' in tags:
        return 'Natural'
    
    # Landuse
    if 'landuse' in tags:
        landuse = tags['landuse'].capitalize()
        if landuse in ['Residential', 'Commercial', 'Industrial', 'Retail']:
            return landuse
        else:
            return f'Landuse: {landuse}'
    
    # If no specific category is found, return 'Other'
    return 'Other'

def parse_osm_data(elements: List[Dict]) -> pd.DataFrame:
    parsed_data = []
    for element in elements:
        tags = element.get('tags', {})
        parsed_element = {
            'ID': f"{element['type']}_{element['id']}",
            'Location Name': tags.get('name', ''),
            'Location Type': determine_location_type(tags)
        }
        parsed_data.append(parsed_element)
    if len(parsed_data) == 0:
        return pd.DataFrame(columns=['ID', 'Location Name', 'Location Type'])
    return pd.DataFrame(parsed_data)

def get_osm_data(lat: float, lon: float, radius: int) -> pd.DataFrame:
    raw_data = fetch_osm_data(lat, lon, radius)
    return parse_osm_data(raw_data)

def dms_to_decimal(coord_str):
    # Regular expression to match the coordinate format
    pattern = r'(\d+)°(\d+)\'([\d.]+)"([NS])\s*(\d+)°(\d+)\'([\d.]+)"([EW])'
    
    match = re.match(pattern, coord_str)
    if not match:
        raise ValueError("Invalid coordinate format. Expected format: 19°03'08.6\"N 72°54'06.0\"E")

    lat_deg, lat_min, lat_sec, lat_dir, lon_deg, lon_min, lon_sec, lon_dir = match.groups()

    # Convert to decimal degrees
    lat = float(lat_deg) + float(lat_min)/60 + float(lat_sec)/3600
    lon = float(lon_deg) + float(lon_min)/60 + float(lon_sec)/3600

    # Adjust sign based on direction
    if lat_dir == 'S':
        lat = -lat
    if lon_dir == 'W':
        lon = -lon

    return lat, lon


def calculate_distant_points(lat: float, lon: float, distance: float) -> tuple:
    # Earth's radius in meters
    R = 6371000

    # Convert latitude and longitude to radians
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)

    # Calculate the point with the same latitude (moving east-west)
    delta_lon = distance / (R * math.cos(lat_rad))
    lon1 = lon + math.degrees(delta_lon)
    
    # Calculate the point with the same longitude (moving north-south)
    delta_lat = distance / R
    lat2 = lat + math.degrees(delta_lat)

    return ((lat, lon1), (lat2, lon))

## 2d map grid (0,0) --> bottom left

def create_map_grid(bottom_left: Tuple[float, float], top_right: Tuple[float, float], rows: int, cols: int) -> List[List[Tuple[float, float]]]:
    grid = []
    lat_unit = (top_right[0] - bottom_left[0]) / rows
    lon_unit = (top_right[1] - bottom_left[1]) / cols
    
    for i in range(rows):
        row = []
        for j in range(cols):
            lat = bottom_left[0] + i * lat_unit
            lon = bottom_left[1] + j * lon_unit
            lat = lat + lat_unit / 2
            lon = lon + lon_unit / 2
            row.append((lat, lon))
        grid.append(row)
    
    return grid

## entire pipeline

# left_lat = 18.889833
# left_lon = 72.779844
# dist = 35

def input_filter(lat=None, lon=None, string=None):
    if lat != None:
        return (lat, lon)
    elif string != None:
        latitude, longitude = dms_to_decimal(string)
        return (latitude, longitude)
    else:
        return None

def get_data(bottom_left_lat, bottom_left_lon, dist):

    result =  calculate_distant_points(bottom_left_lat, bottom_left_lon, 1000*dist)

    top_right_lat = result[1][0]
    top_right_lon = result[0][1]
    grid = create_map_grid((bottom_left_lat, bottom_left_lon), (top_right_lat, top_right_lon), dist, dist)

    grid_dataset = []
    for i, row in enumerate(grid):
        for j, point in enumerate(row):
            result_df = get_osm_data(point[0], point[1], 710)
            # print(result_df.head(3))
            labelled_df = result_df[result_df['Location Type'] != 'Other']
            labelled_df = labelled_df[labelled_df['Location Type'] != 'Religious']
            labelled_df = labelled_df[labelled_df['Location Type'] != 'Transportation']
            loc_types = []
            for row in labelled_df.iterrows():
                loc_type = (row[1]['Location Name'], row[1]['Location Type'])
                if loc_type not in loc_types:
                    loc_types.append(loc_type)

            labelled_df = pd.DataFrame(loc_types, columns=['Location Name', 'Location Type'])

            row_of_dataset = ''

            for row in labelled_df.iterrows():
                row_text = row[1]['Location Name'] + ' is a ' + row[1]['Location Type']
                row_of_dataset += row_text + '; '
            ## replacing any coma in the text with a blank space

            row_of_dataset = row_of_dataset.replace(',', ' ')
            
            grid_row = {"row": i, "col": j, "latitude": point[0], "longitude": point[1], "Map Data": row_of_dataset}
            grid_dataset.append(grid_row)

    grid_df = pd.DataFrame(grid_dataset)
    return grid_df
    # grid_df.to_csv('MMR_DATASET.csv', index=False)