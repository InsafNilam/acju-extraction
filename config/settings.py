"""Configuration settings for the prayer times scraper."""

# URLs
BASE_URL = "https://www.acju.lk/"

# Directories
DOWNLOAD_DIR = "data/prayer_times"
OUTPUT_DIR = "output"

# File names
OUTPUT_FILENAME = "prayer_times_sri_lanka_full.json"

# Data structure
VERSION = "1.0"
DATA_SOURCE = "acju.lk"
TIMEZONE = "Asia/Colombo"
COUNTRY = "Sri Lanka"

# Mapping: filename patterns to city districts
FILENAME_TO_CITY = {
    'colombo': ['COLOMBO-DISTRICT-GAMPAHA-DISTRICT-KALUTARA-DISTRICT'],
    'hambantota': ['HAMBANTOTA-DISTRICT'],
    'ratnapura': ['RATNAPURA-DISTRICT-KEGALLE-DISTRICT'],
    'galle': ['GALLE-DISTRICT-MATARA-DISTRICT'],
    'badulla': ['BADULLA-DISTRICT-MONARAGALA-DISTRICT-PADIYATALAWA-DEHIATHTHAKANDIYA'],
    'trincomalee': ['TRINCOMALEE-DISTRICT'],
    'batticaloa': ['BATTICALOA-DISTRICT-AMPARA-DISTRICT'],
    'kandy': ['KANDY-DISTRICT-MATALE-DISTRICT-NUWARA-ELIYA-DISTRICT'],
    'kurunegala': ['KURUNEGALA-DISTRICT'],
    'anuradhapura': ['ANURADHAPURA-DISTRICT-POLONNARUWA-DISTRICT'],
    'mannar': ['MANNAR-DISTRICT-PUTTALAM-DISTRICT'],
    'vavuniya': ['MULLAITIVU-DISTRICT-EXCEPT-NALLUR-KILINOCHCHI-DISTRICT-VAVUNIYA-DISTRICT'],
    'jaffna': ['JAFFNA-DISTRICT-NALLUR']
}

# Month patterns for extraction
MONTH_PATTERNS = {
    r'\bjanuary\b': '01', r'\bjan\b': '01',
    r'\bfebruary\b': '02', r'\bfeb\b': '02',
    r'\bmarch\b': '03', r'\bmar\b': '03',
    r'\bapril\b': '04', r'\bapr\b': '04',
    r'\bmay\b': '05',
    r'\bjune\b': '06', r'\bjun\b': '06',
    r'\bjuly\b': '07', r'\bjul\b': '07',
    r'\baugust\b': '08', r'\baug\b': '08',
    r'\bseptember\b': '09', r'\bsep\b': '09',
    r'\boctober\b': '10', r'\boct\b': '10',
    r'\bnovember\b': '11', r'\bnov\b': '11',
    r'\bdecember\b': '12', r'\bdec\b': '12',
}

MONTH_NAMES = {
    '01': 'January', '02': 'February', '03': 'March',
    '04': 'April', '05': 'May', '06': 'June',
    '07': 'July', '08': 'August', '09': 'September',
    '10': 'October', '11': 'November', '12': 'December'
}

HIJRI_MONTHS = [
    "Muharram", "Safar", "Rabi al-Awwal", "Rabi al-Thani",
    "Jumada al-Awwal", "Jumada al-Thani", "Rajab", "Shaban",
    "Ramadan", "Shawwal", "Dhu al-Qadah", "Dhu al-Hijjah"
]

# Request settings
REQUEST_TIMEOUT = 20  # seconds