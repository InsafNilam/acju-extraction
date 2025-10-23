"""Main prayer times extractor orchestrator."""

from collections import defaultdict
from typing import Tuple

from src.extractor.pdf_parser import PDFParser
from src.extractor.zone_mapper import ZoneMapper


class PrayerTimesExtractor:
    """Orchestrates extraction of prayer times from PDFs."""
    
    def __init__(self):
        self.pdf_parser = PDFParser()
        self.zone_mapper = ZoneMapper()
        self.all_prayer_times = defaultdict(lambda: defaultdict(dict))
    
    def extract_from_pdf(self, pdf_path: str, filename: str) -> Tuple[str, str, int]:
        """
        Extract prayer times from a single PDF file.
        
        Args:
            pdf_path: Path to PDF file
            filename: Name of PDF file
            
        Returns:
            Tuple of (zone, month, records_count)
        """
        try:
            # Extract text and metadata
            all_text, zone, month = self.pdf_parser.extract_text_and_metadata(pdf_path)
            
            if not zone or not month:
                print(f"    ❌ Could not extract zone/month from {filename}")
                return None, None, 0
            
            print(f"    ✓ Zone: {zone}, Month: {month}")
            
            # Map zone to city
            city_id = self.zone_mapper.build_zone_mapping(zone, filename)
            if not city_id:
                print(f"    ❌ Could not identify city")
                return None, None, 0
            
            records_count = 0
            
            # METHOD 1: Table extraction
            tables = self.pdf_parser.extract_tables(pdf_path)
            print(f"    📊 Found {len(tables)} tables")
            
            for table_idx, table in enumerate(tables):
                prayer_times = self.pdf_parser.parse_table_rows(table, month)
                for prayer_data in prayer_times:
                    date = prayer_data.pop("date")
                    self.all_prayer_times[city_id][date] = prayer_data
                    records_count += 1
            
            # METHOD 2: Text-based fallback
            if records_count == 0:
                print(f"    ⚠ Trying text extraction...")
                prayer_times = self.pdf_parser.extract_from_text_pattern(all_text, month)
                
                for prayer_data in prayer_times:
                    date = prayer_data.pop("date")
                    self.all_prayer_times[city_id][date] = prayer_data
                    records_count += 1
                
                if records_count > 0:
                    print(f"    ✓ Extracted {records_count} records from text")
                else:
                    print(f"    ❌ No records found")
            
            print(f"    📊 Total records: {records_count}")
            return zone, month, records_count
            
        except Exception as e:
            print(f"    ❌ Error: {e}")
            return None, None, 0
    
    def enhance_asr_times(self):
        """Convert ASR times to Shafi/Hanafi structure."""
        for city_id in self.all_prayer_times:
            for date in self.all_prayer_times[city_id]:
                asr_time = self.all_prayer_times[city_id][date].get('asr', '')
                if asr_time:
                    self.all_prayer_times[city_id][date]['asr'] = {
                        'shafi': asr_time,
                        'hanafi': asr_time
                    }
    
    def get_cities_data(self):
        """Get the list of cities processed."""
        return self.zone_mapper.cities_data
    
    def get_prayer_times(self):
        """Get all extracted prayer times."""
        return self.all_prayer_times