"""Date parsing utilities."""

import re


def parse_date(date_str: str, month: str) -> str:
    """
    Convert date string to MM-DD format.
    
    Args:
        date_str: Raw date string from PDF
        month: Month number (01-12)
        
    Returns:
        Formatted date (MM-DD) or None
    """
    try:
        date_str = date_str.strip()
        day_match = re.search(r'\d+', date_str)
        if day_match:
            day = int(day_match.group())
            return f"{month}-{day:02d}"
    except Exception:
        pass
    return None


def natural_sort_key(s: str):
    """
    Generate natural sorting key for strings with numbers.
    
    Args:
        s: String to sort
        
    Returns:
        List of strings and integers for natural sorting
    """
    return [int(text) if text.isdigit() else text.lower() 
            for text in re.split(r'(\d+)', s)]