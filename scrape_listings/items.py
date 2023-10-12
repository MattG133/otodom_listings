# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ListingsPage(scrapy.Item):
    title = scrapy.Field()
    address = scrapy.Field()
    price = scrapy.Field()
    area = scrapy.Field()
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