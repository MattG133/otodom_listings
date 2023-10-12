# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from scrapy.exporters import CsvItemExporter
from itemadapter import ItemAdapter
from scrape_listings.items import ListingsPage, ListingItems
import csv

class ScrapeListingsPipeline:
    def process_item(self, item, spider):
        return item

class CsvExportPipeline1:
    def __init__(self):
        self.file = open('../scrape_listings/data/raw/listings_page.csv', 'w', newline='', encoding='utf-8')
        self.exporter = csv.DictWriter(self.file, fieldnames=['title', 'address', 'price', 'area', 'link1'])  # Replace with your fieldnames
        self.exporter.writeheader()

    def process_item(self, item, spider):
        # Check if the item belongs to the first Item class
        if isinstance(item, ListingsPage):
            self.exporter.writerow(item)
        return item

    def close_spider(self, spider):
        self.file.close()

class CsvExportPipeline2:
    def __init__(self):
        self.file = open('../scrape_listings/data/raw/listings_item.csv', 'w', newline='', encoding='utf-8')
        self.exporter = csv.DictWriter(self.file, fieldnames=['rooms_No', 'ownership_form', 'interior_state', 'floor', 'balcony', 'parking_space', 'listing_type', 'description', 'year_built', 'building_type', 'lift', 'link2'])  # Replace with your fieldnames
        self.exporter.writeheader()

    def process_item(self, item, spider):
        # Check if the item belongs to the second Item class
        if isinstance(item, ListingItems):
            self.exporter.writerow(item)
        return item

    def close_spider(self, spider):
        self.file.close()

