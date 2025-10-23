"""File I/O utilities."""

import json
import shutil
from datetime import datetime
from typing import Dict

from config.settings import VERSION, DATA_SOURCE, TIMEZONE


def generate_output_json(cities_data: list, prayer_times: dict) -> dict:
    """
    Generate the complete JSON structure.
    
    Args:
        cities_data: List of city metadata
        prayer_times: Dictionary of prayer times by city
        
    Returns:
        Complete structured data dictionary
    """
    prayer_times_structure = {}
    
    for city_id, city_times in prayer_times.items():
        prayer_times_structure[city_id] = {
            'timezone': TIMEZONE,
            'times': city_times
        }
    
    complete_data = {
        'version': VERSION,
        'last_updated': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'data_source': DATA_SOURCE,
        'cities': cities_data,
        'prayer_times': prayer_times_structure
    }
    
    return complete_data


def save_json(data: Dict, filename: str) -> bool:
    """
    Save data to JSON file.
    
    Args:
        data: Dictionary to save
        filename: Output filename
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Data saved to {filename}")
        return True
    except Exception as e:
        print(f"❌ Error saving: {e}")
        return False


def cleanup_directory(directory: str):
    """
    Remove a directory and all its contents.
    
    Args:
        directory: Path to directory to remove
    """
    try:
        shutil.rmtree(directory)
        print(f"🧹 Deleted temporary folder '{directory}'")
    except Exception as e:
        print(f"⚠️ Could not delete {directory}: {e}")