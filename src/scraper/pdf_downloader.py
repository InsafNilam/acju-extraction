"""PDF downloader for prayer times."""

import os
import requests
import time
import random
from typing import List, Optional


class PDFDownloader:
    """Download PDF files from URLs."""
    
    def __init__(self, download_dir="data/prayer_times", max_retries=3, backoff_factor=2):
        self.download_dir = download_dir
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        os.makedirs(download_dir, exist_ok=True)
    
    def download_pdfs(self, scraped_data: List[dict], months: Optional[List[str]] = None) -> List[str]:
        """
        Download all PDF files from scraped prayer time links.
        
        Args:
            scraped_data: List of dictionaries containing section and items
            month: Optional month string (e.g., 'January')
            
        Returns:
            List of downloaded file paths
        """
        downloaded_files = []
        months_lower = [m.lower() for m in months] if months else None

        for section in scraped_data:
            for item in section["items"]:
                item_month = item.get("month", "").lower()
                if months_lower and item_month not in months_lower:
                    continue

                filepath = self._download_single_pdf(item)
                if filepath:
                    downloaded_files.append(filepath)

                time.sleep(random.uniform(0.5, 1.5))

        return downloaded_files
    
    def _download_single_pdf(self, item: dict) -> str:
        """
        Download a single PDF file.
        
        Args:
            item: Dictionary with 'link' key
            
        Returns:
            File path if successful, None otherwise
        """
        link = item.get("link")
        if not link or not link.lower().endswith(".pdf"):
            return None
        
        filename = os.path.basename(link.split("?")[0])
        filepath = os.path.join(self.download_dir, filename)
        
        for attempt in range(1, self.max_retries + 1):
            try:
                print(f"⬇️ Downloading {filename} ...")
                response = requests.get(link)
                response.raise_for_status()
                
                with open(filepath, "wb") as f:
                    f.write(response.content)
                
                return filepath
                
            except requests.RequestException as e:
                wait_time = self.backoff_factor ** attempt
                print(f"❌ Failed to download {filename}: {e}. Retrying in {wait_time:.1f}s...")
                time.sleep(wait_time)
        
        print(f"⚠️ Max retries exceeded for {filename}. Skipping.")
        return None