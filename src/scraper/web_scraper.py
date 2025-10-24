"""Web scraper for ACJU prayer times website."""

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.settings import BASE_URL, REQUEST_TIMEOUT
from src.utils.date_utils import parse_hijri_day


class ACJUWebScraper:
    """Scraper for ACJU prayer times PDF links."""
    
    def __init__(self, base_url=BASE_URL):
        self.prayer_base_url = base_url + "prayer-times/"
        self.calendar_url = base_url + "calenders-en/"
    
    def get_districts(self):
        """
        Extract prayer time section names and corresponding location data.
        
        Returns:
            list: List of dictionaries containing section and items data
        """
        try:
            response = requests.get(self.prayer_base_url, timeout=REQUEST_TIMEOUT)
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
    
    def get_acju_calendar(self):
        """
        Scrapes Hijri and Gregorian date information from ACJU's calendar page.
        Returns a structured dictionary with both Hijri and Gregorian data.
        """
        driver = None

        try:
            # 🧩 Setup Chrome in headless mode
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

            driver = webdriver.Chrome(options=chrome_options)
            driver.get(self.calendar_url)

            # ⏳ Wait for the calendar to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "calendar-header"))
            )

            soup = BeautifulSoup(driver.page_source, "html.parser")

            # 🌙 Hijri elements
            hijri_month_raw = soup.select_one("#hijri-month-name")
            hijri_today_raw = soup.select_one("#calendar #days #today .hijri-date")

            # ☀️ Gregorian element
            gregorian_month_raw = soup.select_one("#gregorian-month-name")

            # --- Extract Hijri month and year ---
            hijri_month_name, hijri_year = None, None
            if hijri_month_raw:
                parts = hijri_month_raw.get_text(strip=True).split()
                if len(parts) >= 2:
                    hijri_month_name = " ".join(parts[:-1])
                    try:
                        hijri_year = int(parts[-1])
                    except ValueError:
                        pass

            # --- Extract Hijri day (handles "30/1") ---
            hijri_today_text = hijri_today_raw.get_text(strip=True) if hijri_today_raw else None
            hijri_info = parse_hijri_day(hijri_today_text, hijri_month_name)

            # --- Extract Gregorian date ---
            gregorian_text = gregorian_month_raw.get_text(strip=True).replace("Today:", "").strip() if gregorian_month_raw else ""
            formatted_date = None

            if gregorian_text:
                try:
                    date_obj = datetime.strptime(gregorian_text, "%A, %B %d, %Y")
                    formatted_date = date_obj.strftime("%Y-%m-%d")
                except ValueError:
                    formatted_date = gregorian_text  # fallback

            return {
                "hijri": {
                    **hijri_info,
                    "year": hijri_year,
                },
                "date": formatted_date,
            }

        except Exception as e:
            print(f"⚠️ Error fetching ACJU calendar: {e}")
            return {}
        finally:
            if driver:
                driver.quit()
    
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
                link = requests.compat.urljoin(self.prayer_base_url, link)
            
            return {
                "month": month_text,
                "link": link
            }
        
        return None