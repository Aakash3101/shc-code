import requests

WMS_URL = "https://soilhealth.dac.gov.in/jW8X3zM5Y7pQvLr4K2Tn6HqPbD0tZmN9R6JfO1wCiG8xV5eTk2CdMoF9YsQr0Z7LmN1YxU4pTb2K5LvHqX7F3aCmGzR4Pw0D8UtYnJ9oZ2SvNlQ7Tz1PjR5LcX0Qf8HkV9OrG4V7YxU3pJk6TnMm5CdX8B9tRi1Lw2Qn7F4ZzJk8WvP1GrZ6Sx0JoH5C3oV7fNi2/shc/wms/wms"
CRS = "EPSG:4326"


def get_feature_info(lat, long, layer_names):
    """
    Fetches feature information from the WMS server for a given latitude and longitude.

    Args:
        lat (float): Latitude of the point.
        long (float): Longitude of the point.
        layer_names (list): List of layer names to query.

    Returns:
        dict: JSON response containing feature information.
    """

    bbox = [long - 0.000001, lat - 0.000001, long + 0.000001, lat + 0.000001]

    styles = ""

    params = {
        "SERVICE": "WMS",
        "VERSION": "1.1.1",
        "REQUEST": "GetFeatureInfo",
        "LAYERS": ",".join(map(str, layer_names)),
        "QUERY_LAYERS": ",".join(map(str, layer_names)),
        "HIDE_GEOMETRY": "true",
        "STYLES": styles,
        "SRS": CRS,
        "BBOX": ",".join(map(str, bbox)),
        "X": "5",
        "Y": "5",
        "WIDTH": "11",
        "HEIGHT": "11",
        "INFO_FORMAT": "application/json",
        "FEATURE_COUNT": "10",
        "TRANSPARENT": "false",
    }

    response = requests.get(WMS_URL, params=params)
    if response.status_code == 200:
        try:
            _ = response.json()
        except:
            print(params)
            # print(response.text)
        return response.json()
    else:
        print(f"Status: {response.status_code}, Failed to fetch feature info")
        return None


def convert_px_to_latlong(x, y, bbox, tile_size):
    """
    Converts pixel coordinates to latitude and longitude based on the bounding box and tile size.

    Args:
        x (int): X pixel coordinate.
        y (int): Y pixel coordinate.
        bbox (list): Bounding box in the format [minx, miny, maxx, maxy].
        tile_size (int): Size of the tile in pixels.

    Returns:
        tuple: Latitude and longitude corresponding to the pixel coordinates.
    """

    minx, miny, maxx, maxy = bbox
    res_x = (maxx - minx) / tile_size
    res_y = (maxy - miny) / tile_size

    lat = maxx - (y * res_x)
    long = miny + (x * res_y)

    return lat, long


def pxbbox_to_latlongbbox(bbox, global_bbox, tile_size):
    """
    Converts a bounding box defined in pixel coordinates to latitude and longitude coordinates.

    Args:
        bbox (list): Bounding box in pixel coordinates [x, y, w, h].
        global_bbox (list): Global bounding box in the format [minx, miny, maxx, maxy].
        tile_size (int): Size of the tile in pixels.

    Returns:
        tuple: Bounding box in latitude and longitude coordinates (minx, miny, maxx, maxy).
    """
    x, y, w, h = bbox
    minx, miny, maxx, maxy = global_bbox
    res_x = (maxx - minx) / tile_size
    res_y = (maxy - miny) / tile_size

    new_minx = maxx - ((y + h) * res_x)
    new_miny = miny + (x * res_y)
    new_maxx = maxx - (y * res_x)
    new_maxy = miny + ((x + w) * res_y)

    return new_minx, new_miny, new_maxx, new_maxy
