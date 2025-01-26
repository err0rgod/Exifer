from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os

def print_logo():
    print("""
 /$$$$$$$$           /$$  /$$$$$$                   
| $$_____/          |__/ /$$__  $$                  
| $$       /$$   /$$ /$$| $$  \__//$$$$$$   /$$$$$$ 
| $$$$$   |  $$ /$$/| $$| $$$$   /$$__  $$ /$$__  $$
| $$__/    \  $$$$/ | $$| $$_/  | $$$$$$$$| $$  \__/
| $$        >$$  $$ | $$| $$    | $$_____/| $$      
| $$$$$$$$ /$$/\  $$| $$| $$    |  $$$$$$$| $$      
|________/|__/  \__/|__/|__/     \_______/|__/      
                                                  
 /$$                                                      /$$$$$$                                      /$$
| $$                                                     /$$$_  $$                                    | $$
| $$$$$$$  /$$   /$$        /$$$$$$   /$$$$$$   /$$$$$$ | $$$$\ $$  /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$$
| $$__  $$| $$  | $$       /$$__  $$ /$$__  $$ /$$__  $$| $$ $$ $$ /$$__  $$ /$$__  $$ /$$__  $$ /$$__  $$
| $$  \ $$| $$  | $$      | $$$$$$$$| $$  \__/| $$  \__/| $$\ $$$$| $$  \__/| $$  \ $$| $$  \ $$| $$  | $$
| $$  | $$| $$  | $$      | $$_____/| $$      | $$      | $$ \ $$$| $$      | $$  | $$| $$  | $$| $$  | $$
| $$$$$$$/|  $$$$$$$      |  $$$$$$$| $$      | $$      |  $$$$$$/| $$      |  $$$$$$$|  $$$$$$/|  $$$$$$$
|_______/  \____  $$       \_______/|__/      |__/       \______/ |__/       \____  $$ \______/  \_______/
           /$$  | $$                                                         /$$  \ $$                    
          |  $$$$$$/                                                        |  $$$$$$/                    
           \______/                                                          \______/                     
                                                                                                          
                                                   
    
    """)

def write_exif_data(exif_data, file_path):
    with open(file_path, 'w') as f:
        for tag, value in exif_data.items():
            if isinstance(value, bytes):
                value = value.decode()
            f.write(f"{tag}: {value}\n")

def get_maps_url(GPSInfo):
    # Define the GPS coordinates
    lat_degrees, lat_minutes, lat_seconds = GPSInfo['GPSLatitude']
    lon_degrees, lon_minutes, lon_seconds = GPSInfo['GPSLongitude']
    
    # Calculate the latitude and longitude in decimal degrees
    latitude = lat_degrees + lat_minutes/60 + lat_seconds/3600.0
    if GPSInfo['GPSLatitudeRef'] == 'S':
        latitude = -latitude
    longitude = lon_degrees + lon_minutes/60 + lon_seconds/3600.0
    if GPSInfo['GPSLongitudeRef'] == 'W':
        longitude = -longitude
    
    # Create the Google Maps URL
    maps_url = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"

    # Return the URL
    return maps_url


def get_exif_data(image_path):
    image = Image.open(image_path)
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for gps_tag in value:
                    sub_decoded = GPSTAGS.get(gps_tag, gps_tag)
                    gps_data[sub_decoded] = value[gps_tag]
                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    # Print specific EXIF data
    print("\nMake:", exif_data.get("Make"))
    print("Model:", exif_data.get("Model"))
    print("GPS Coordinates:", exif_data.get("GPSInfo"))
    print("Date/Time:", exif_data.get("DateTimeOriginal"))
    print("Image Resolution:", exif_data.get("ExifImageWidth"), "x", exif_data.get("ExifImageHeight"))
    print("Exposure Time:", exif_data.get("ExposureTime"), "seconds")
    print("Aperture:", "f/", exif_data.get("FNumber"))
    print("ISO Speed:", exif_data.get("ISOSpeedRatings"))
    print("Lens Model:", exif_data.get("LensModel"))
    print("Flash Used:", "Yes" if exif_data.get("Flash") else "No")
    print("Orientation:", exif_data.get("Orientation"))
    print("Image Format:", exif_data.get("MimeType"))
    print("Image Description:", exif_data.get("ImageDescription"))
    print("Keywords:", exif_data.get("Keywords"))
    print("Copyright:", exif_data.get("Copyright"))
    print("Google Maps link:", get_maps_url(exif_data.get("GPSInfo")))

    #save to file
    exif_data['Google Maps link'] = get_maps_url(exif_data.get("GPSInfo"))
    out_file = image_path.split(".")[0]
    write_exif_data(exif_data, f'{out_file}.txt')

    print(f'\nEXIF data printed to {out_file}.txt')

def main():
    print_logo()
    path = input("enter path to img file: \n")
    if os.path.exists(path):
        try:
            get_exif_data(path)
        except:
            print("no EXIF data found")
    else:
        print("invalid file")

main()
