# image_metadata_processor.py

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

class ImageMetadataProcessor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.exif_data = {}
        self.labeled_exif = {}
        self.location_info = {}

    def process(self):
        self._get_exif_data()
        self._get_labeled_exif()
        self._get_location_info()

    def _get_exif_data(self):
        try:
            image = Image.open(self.image_path)
        except Exception as e:
            print(f"이미지를 열 수 없습니다: {e}")
            return

        info = image._getexif()
        
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                self.exif_data[decoded] = value
                
                if decoded == "GPSInfo":
                    gps_data = {}
                    for t in value:
                        sub_decoded = GPSTAGS.get(t, t)
                        gps_data[sub_decoded] = value[t]
                    self.exif_data[decoded] = gps_data
        else:
            print("EXIF 정보를 찾을 수 없습니다.")

    def _get_labeled_exif(self):
        if "DateTimeOriginal" in self.exif_data:
            self.labeled_exif["Date/Time"] = self.exif_data["DateTimeOriginal"]
        else:
            print("날짜 및 시간 정보를 찾을 수 없습니다.")
        
        if "GPSInfo" in self.exif_data:
            gps_info = self.exif_data["GPSInfo"]
            gps_lat = gps_info.get("GPSLatitude")
            gps_lat_ref = gps_info.get("GPSLatitudeRef")
            gps_lon = gps_info.get("GPSLongitude")
            gps_lon_ref = gps_info.get("GPSLongitudeRef")
            
            if gps_lat and gps_lat_ref and gps_lon and gps_lon_ref:
                lat = self._convert_to_degrees(gps_lat)
                if gps_lat_ref != "N":
                    lat = -lat
                self.labeled_exif["Latitude"] = lat
                
                lon = self._convert_to_degrees(gps_lon)
                if gps_lon_ref != "E":
                    lon = -lon
                self.labeled_exif["Longitude"] = lon
            else:
                print("GPS 정보를 찾을 수 없습니다.")
        else:
            print("GPS 정보를 찾을 수 없습니다.")

    @staticmethod
    def _convert_to_degrees(value):
        d = float(value[0])
        m = float(value[1])
        s = float(value[2])
        
        return d + (m / 60.0) + (s / 3600.0)

    def _get_location_info(self):
        if "Latitude" in self.labeled_exif and "Longitude" in self.labeled_exif:
            geolocator = Nominatim(user_agent="my_app")
            
            try:
                location = geolocator.reverse(f"{self.labeled_exif['Latitude']}, {self.labeled_exif['Longitude']}")
                address = location.raw['address']
                
                self.location_info = {
                    "full_address": location.address,
                    "country": address.get('country', ''),
                    "state": address.get('state', ''),
                    "city": address.get('city', address.get('town', address.get('village', ''))),
                    "suburb": address.get('suburb', ''),
                    "road": address.get('road', ''),
                    "house_number": address.get('house_number', ''),
                    "postcode": address.get('postcode', '')
                }
            except GeocoderTimedOut:
                print("지오코딩 서비스 시간 초과. 다시 시도해주세요.")
            except Exception as e:
                print(f"위치 정보를 가져오는 데 실패했습니다: {e}")
        else:
            print("GPS 정보를 찾을 수 없어 위치 정보를 가져올 수 없습니다.")

    def print_results(self):
        print("추출된 EXIF 데이터:", self.exif_data)
        print("라벨링된 EXIF 데이터:", self.labeled_exif)
        if self.location_info:
            print("위치 정보:")
            for key, value in self.location_info.items():
                print(f"{key}: {value}")
        else:
            print("위치 정보를 가져올 수 없습니다.")