"""Date parsing utilities."""

import re
from config.settings import HIJRI_MONTHS


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

def parse_hijri_day(day_text: str, current_month: str):
    """Parse Hijri day text (e.g., '30' or '30/1') into structured data."""
    if not day_text:
        return {"day": None, "month": current_month, "post": None}

    hijri_day, post_day = None, None

    if "/" in day_text:
        parts = [p.strip() for p in day_text.split("/") if p.strip()]
        if parts and parts[0].isdigit():
            hijri_day = int(parts[0])
        if len(parts) > 1 and parts[1].isdigit():
            post_day = int(parts[1])
    elif day_text.isdigit():
        hijri_day = int(day_text)

    post = None
    if post_day:
        current_idx = HIJRI_MONTHS.index(current_month) if current_month in HIJRI_MONTHS else -1
        if current_idx >= 0:
            next_month = HIJRI_MONTHS[(current_idx + 1) % len(HIJRI_MONTHS)]
            post = {"day": post_day, "month": next_month}

    return {"day": hijri_day, "month": current_month, "post": post}


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