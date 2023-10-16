# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ListingsPage(scrapy.Item):
    title = scrapy.Field()
    address = scrapy.Field()
    price = scrapy.Field()
    link1 = scrapy.Field()
    

class ListingItems(scrapy.Item):
    rooms_No = scrapy.Field()
    ownership_form = scrapy.Field()
    interior_state = scrapy.Field()
    floor = scrapy.Field()
    balcony = scrapy.Field()
    parking_space = scrapy.Field()
    listing_type = scrapy.Field()
    description = scrapy.Field()
    year_built = scrapy.Field()
    building_type = scrapy.Field()
    lift = scrapy.Field()
    link2 = scrapy.Field()
    market = scrapy.Field()
    advertiser_type = scrapy.Field()
    available_from = scrapy.Field()
    year_of_construction = scrapy.Field()
    building_type = scrapy.Field()
    windows = scrapy.Field()
    elevator = scrapy.Field()
    utilities = scrapy.Field()
    security = scrapy.Field()
    equipment = scrapy.Field()
    additional_info = scrapy.Field()
    building_material = scrapy.Field()
    listing_ID = scrapy.Field()
    area = scrapy.Field()
    
class RentListingsPage(scrapy.Item):
    title = scrapy.Field()
    address = scrapy.Field()
    rent = scrapy.Field()
    area = scrapy.Field()
    link1 = scrapy.Field()
    
class RentListingItems(scrapy.Item):
    area = scrapy.Field()
    rooms_No = scrapy.Field()
    floor = scrapy.Field()
    available_from = scrapy.Field()
    remote_service = scrapy.Field()
    fees = scrapy.Field()
    deposit = scrapy.Field()
    building_type = scrapy.Field()
    link2 = scrapy.Field()
    balcony = scrapy.Field()
    interior_state = scrapy.Field()
    description = scrapy.Field()
    listing_ID = scrapy.Field()
    
class ListingImages(scrapy.Item):
    images = scrapy.Field()
    listing_url = scrapy.Field()