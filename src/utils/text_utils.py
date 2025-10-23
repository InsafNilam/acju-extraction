"""Text parsing and cleaning utilities."""

import re
from config.settings import MONTH_PATTERNS, MONTH_NAMES
from typing import Optional


def extract_zone_from_text(text: str) -> str:
    """
    Extract zone number from PDF text.
    
    Args:
        text: PDF text content
        
    Returns:
        Zone number (zero-padded) or None
    """
    zone_pattern = r'Zone:\s*(\d+)'
    match = re.search(zone_pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).zfill(2)
    return None


def extract_month_from_text(text: str) -> str:
    """
    Extract month from PDF text using word boundaries.
    
    Args:
        text: PDF text content
        
    Returns:
        Month number (01-12) or None
    """
    text_lower = text.lower()
    
    for pattern, month_num in MONTH_PATTERNS.items():
        match = re.search(pattern, text_lower)
        if match:
            matched_text = match.group(0)
            print(f"    ✓ Found month: {matched_text} → {month_num}")
            return month_num
    
    return None

def normalize_month(month_input: str) -> Optional[str]:
    """Normalize user input like 'jan', 'JAN', '3' → 'March'."""
    if not month_input:
        return None
    text = month_input.strip().lower()

    # Numeric support (e.g., '3' or '03')
    if text.isdigit():
        text = text.zfill(2)
        return MONTH_NAMES.get(text)

    # Regex pattern match (e.g., 'jan', 'march')
    for pattern, code in MONTH_PATTERNS.items():
        if re.search(pattern, text):
            return MONTH_NAMES[code]

    return None


def clean_time(time_str) -> str:
    """
    Clean and format time string.
    
    Args:
        time_str: Raw time string
        
    Returns:
        Cleaned time string
    """
    try:
        if time_str:
            return str(time_str).strip()
        return ""
    except Exception:
        return ""