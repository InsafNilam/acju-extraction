"""Web scraper for ACJU prayer times website."""

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from config.settings import BASE_URL, REQUEST_TIMEOUT


class ACJUWebScraper:
    """Scraper for ACJU prayer times PDF links."""
    
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
    
    def get_districts(self):
        """
        Extract prayer time section names and corresponding location data.
        
        Returns:
            list: List of dictionaries containing section and items data
        """
        try:
            response = requests.get(self.base_url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            details_elements = soup.select("div.e-n-accordion details")
            
            if not details_elements:
                print("⚠️ No matching elements found.")
                return []
            
            results = []
            
            for detail in tqdm(details_elements, desc="Extracting prayer time sections"):
                section_data = self._extract_section_data(detail)
                if section_data:
                    results.append(section_data)
            
            return results
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching data: {e}")
            return []
    
    def _extract_section_data(self, detail):
        """
        Extract data from a single detail element.
        
        Args:
            detail: BeautifulSoup element
            
        Returns:
            dict: Section data with name and items
        """
        section_span = detail.select_one("summary span:first-child")
        section_name = section_span.get_text(strip=True) if section_span else "Unknown Section"
        
        region_div = detail.select_one("div[role='region']")
        if not region_div:
            return None
        
        month_rows = region_div.select(":scope > div")
        items = []
        
        for row in month_rows:
            item = self._extract_month_item(row)
            if item:
                items.append(item)
        
        return {
            "section": section_name,
            "items": items
        }
    
    def _extract_month_item(self, row):
        """
        Extract month and PDF link from a row.
        
        Args:
            row: BeautifulSoup element
            
        Returns:
            dict: Month and link data or None
        """
        month = row.select_one("div:nth-child(1) p span")
        month_text = month.get_text(strip=True) if month else None
        
        link = next(
            (a["href"].strip() for a in row.select("a[href]")
             if a["href"].lower().endswith(".pdf")),
            None
        )
        
        if month_text and link:
            if link.startswith("/"):
                link = requests.compat.urljoin(self.base_url, link)
            
            return {
                "month": month_text,
                "link": link
            }
        
        return None