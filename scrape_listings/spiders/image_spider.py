import scrapy
import pprint
from urllib.parse import urlsplit
from urllib.parse import urlparse
import json
from scrape_listings.items import ListingImages
import os
import hashlib
import pdb
import time



class ImagesSpider(scrapy.Spider):
    name = 'images'
    start_urls = ['https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa/warszawa/warszawa?viewType=listing&page=1']
    max_pages = 2

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrape_listings.middlewares.RotateUserAgentMiddleware': 400,
            # Add other middleware settings if needed
        },
    }

    def find_image_urls(self, data, prop):
        image_urls = []

        if isinstance(data, dict):
            for key, value in data.items():
                if key == prop:
                    if isinstance(value, list):
                        image_urls.extend(value)
                    elif isinstance(value, str):
                        image_urls.append(value)
                else:
                    image_urls.extend(self.find_image_urls(value, prop))
        elif isinstance(data, list):
            for item in data:
                image_urls.extend(self.find_image_urls(item, prop))

        return image_urls
    
    def url_to_unique_id(self, url):
        # Create an MD5 hash object
        hash_object = hashlib.md5()
    
        # Encode the URL as bytes (UTF-8 encoding)
        url_bytes = url.encode('utf-8')
    
        # Update the hash object with the URL bytes
        hash_object.update(url_bytes)
    
        # Get the hexadecimal representation of the hash
        unique_id = hash_object.hexdigest()
    
        return unique_id

    def parse(self, response):
        # Extract links to individual listing pages
        listing_links = response.css('a[data-cy="listing-item-link"]::attr(href)').getall()
        #print("LISTINGS ON THE PAGE !!!!!!!!!!!!!!!!!!!! {listing_links}")
        for listing_link in listing_links:
            # Check if the URL has a scheme, and validate the URL
            url_parts = urlsplit(listing_link)
            if not url_parts.scheme:
                listing_link = 'https://www.otodom.pl' + listing_link

            yield scrapy.Request(url=listing_link, callback=self.parse_listing)
        #pdb.set_trace()
        # Locate the next page button
        next_page_button = response.css('button[data-cy="pagination.next-page"]')
        if next_page_button and self.max_pages > 1:
            # Get the URL for the next page
            next_page_url = next_page_button.css('::attr(href)').get()

            # Ensure that next_page_url is not None before following
            if next_page_url:
                yield response.follow(next_page_url, self.parse, cb_kwargs={'max_pages': self.max_pages - 1})
    
    def parse_listing(self, response):
        # Extract the JSON data containing image information
        json_data = response.css('script[id="__NEXT_DATA__"]::text').get()
        data = json.loads(json_data)
        #print(data['props']['pageProps']['images'])
        
        # Convert URL to hash
        listing_url = response.request.url
        listing_id = self.url_to_unique_id(listing_url)

        # Extract the "medium" images
        image_urls = self.find_image_urls(data, "images")
        medium_images = [image['medium'] for image in image_urls]

        for idx, image_url in enumerate(medium_images, start=1):
            yield scrapy.Request(image_url, callback=self.save_image, meta={'listing_id': listing_id, 'image_index': idx})

    def save_image(self, response):
        # Extract the listing ID and image index from the meta data
        listing_id = response.meta['listing_id']
        image_index = response.meta['image_index']

        # Construct the filename with listing ID and image index
        filename = f'{listing_id}_{image_index}.jpg'

        # Define the directory path where you want to save the images
        save_dir = os.path.join("../", "scrape_listings", "data", "images")

        # Create the directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)

        # Construct the full file path
        file_path = os.path.join(save_dir, filename)

        # Save the image as a JPG file
        with open(file_path, 'wb') as f:
            f.write(response.body)

        self.log(f'Saved file {file_path}')    
        
