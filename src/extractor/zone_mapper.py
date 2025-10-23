"""Zone and city mapping utilities."""

from config.settings import FILENAME_TO_CITY, TIMEZONE, COUNTRY


class ZoneMapper:
    """Map zones to cities and maintain city metadata."""
    
    def __init__(self):
        self.zone_mapping = {}
        self.zone_to_filename = {}
        self.cities_data = []
    
    def identify_city_from_filename(self, filename: str) -> str:
        """
        Identify city from filename.
        
        Args:
            filename: PDF filename
            
        Returns:
            City ID or None
        """
        filename_upper = filename.upper()
        for city_id, patterns in FILENAME_TO_CITY.items():
            for pattern in patterns:
                if pattern in filename_upper:
                    return city_id
        return None
    
    def build_zone_mapping(self, zone: str, filename: str) -> str:
        """
        Build zone mapping dynamically.
        
        Args:
            zone: Zone number
            filename: PDF filename
            
        Returns:
            City ID or None
        """
        city_id = self.identify_city_from_filename(filename)
        if city_id and zone:
            city_info = {
                'id': city_id,
                'name': city_id.title(),
                'country': COUNTRY,
                'timezone': TIMEZONE
            }
            self.zone_mapping[zone] = city_info
            self.zone_to_filename[zone] = filename
            
            # Add to cities_data if not already present
            if not any(city['id'] == city_id for city in self.cities_data):
                self.cities_data.append(city_info)
            
            return city_id
        return None
    
    def get_city_info(self, zone: str) -> dict:
        """Get city information for a zone."""
        return self.zone_mapping.get(zone)