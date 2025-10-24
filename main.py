"""Main entry point for prayer times scraper."""

import os
import json
import argparse

from config.settings import DOWNLOAD_DIR, OUTPUT_DIR, OUTPUT_FILENAME
from src.scraper.web_scraper import ACJUWebScraper
from src.scraper.pdf_downloader import PDFDownloader
from src.extractor.time_extractor import PrayerTimesExtractor
from src.utils.file_utils import generate_output_json, save_json, cleanup_directory
from src.utils.date_utils import natural_sort_key
from src.utils.text_utils import normalize_month


def print_extraction_summary(extractor: PrayerTimesExtractor):
    """Print summary of extracted data."""
    print("\n📊 Extraction Summary")
    prayer_times = extractor.get_prayer_times()
    
    for city_id, city_data in prayer_times.items():
        total_days = len(city_data)
        months = sorted({d.split('-')[0] for d in city_data.keys()})
        print(f"  • {city_id.title()}: {total_days} days across months {', '.join(months)}")


def main():
    """Main execution flow."""
    parser = argparse.ArgumentParser(description="ACJU Prayer Times Downloader & Extractor")
    parser.add_argument(
        "--mode",
        choices=["prayer", "calendar"],
        default="prayer",
        help="Select mode: 'prayer' to download & extract prayer times, or 'calendar' to scrape today's calendar info."
    )
    parser.add_argument(
        "--month",
        nargs="*",
        help="Month(s) to download (e.g., 'jan', 'feb', 'march'). Leave empty for all months.",
    )
    args = parser.parse_args()
    scraper = ACJUWebScraper()

    if args.mode == "calendar":
        # --- Run calendar extraction mode ---
        print("📅 Running ACJU Calendar Scraper...")
        calendar_data = scraper.get_acju_calendar()
        print(json.dumps(calendar_data))
        return

    # --- Run prayer times extraction mode ---
    # Normalize all month inputs
    months = None
    if args.month:
        normalized = [normalize_month(m) for m in args.month if normalize_month(m)]
        if not normalized:
            print(f"⚠️ No valid months recognized from input: {args.month}")
            return
        months = normalized
    
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Step 1: Scrape website for PDF links
    print("🌐 Fetching district PDF links from ACJU website...")
    scraped_data = scraper.get_districts()
    
    if not scraped_data:
        print("❌ No data scraped!")
        return
    
    print(f"✅ Found {len(scraped_data)} districts")
    
    # Step 2: Download PDFs
    downloader = PDFDownloader(DOWNLOAD_DIR)
    downloaded_files = downloader.download_pdfs(scraped_data, months=months)
    
    if not downloaded_files:
        print("❌ No PDFs downloaded!")
        return
    
    print(f"✅ Downloaded {len(downloaded_files)} PDF files\n")
    
    # Step 3: Extract prayer times from PDFs
    extractor = PrayerTimesExtractor()
    
    for idx, filepath in enumerate(sorted(downloaded_files, key=natural_sort_key)):
        filename = os.path.basename(filepath)
        print(f"📄 [{idx + 1}/{len(downloaded_files)}] Processing {filename}...")
        
        zone, month, records = extractor.extract_from_pdf(filepath, filename)
        
        if zone and month:
            print(f"  → Zone: {zone}, Month: {month}, Records: {records}\n")
        else:
            print(f"  → Skipped: {filename}\n")
    
    # Step 4: Enhance ASR times
    extractor.enhance_asr_times()
    
    # Step 5: Print summary
    print_extraction_summary(extractor)
    
    # Step 6: Generate and save JSON
    complete_data = generate_output_json(
        extractor.get_cities_data(),
        extractor.get_prayer_times()
    )
    
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
    save_json(complete_data, output_path)
    
    # Step 7: Cleanup temporary files
    if os.path.exists(DOWNLOAD_DIR):
        cleanup_directory(DOWNLOAD_DIR)
    
    print(f"\n🎉 Done! Final dataset saved as '{output_path}'")


if __name__ == "__main__":
    main()