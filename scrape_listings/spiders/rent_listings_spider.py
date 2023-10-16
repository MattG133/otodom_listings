from pathlib import Path
from scrape_listings.pipelines import CsvExportPipeline3, CsvExportPipeline4
from scrape_listings.items import RentListingItems, RentListingsPage
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
import scrapy
import hashlib

class ListingsSpider(scrapy.Spider):
    name = 'rent_listings'

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrape_listings.middlewares.RotateUserAgentMiddleware': 400,
            # Add other middleware settings if needed
        },
    }

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

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        start_urls = [
            f'https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/mazowieckie/warszawa?viewType=listing&page={page}'
            for page in range(1, 168)  # Generate URLs for pages 1 to 300
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response):
        listings = response.css('li[data-cy="listing-item"]')

        for listing in listings:
            item = RentListingsPage()
            
            # Extract the title of the listing
            title = listing.css('span[data-cy="listing-item-title"]::text').get()
            item['title'] = title.strip() if title else 'no info'

            # Extract the address of the listing
            address = listing.css('p.css-19dkezj.e1n06ry53::text').get()
            item['address'] = address.strip() if address else 'no info'

            # Extract the price of the listing
            price = listing.css('span.css-1cyxwvy.ei6hyam2::text').get()
            item['rent'] = price.strip() if price else 'no info'

            # Extract the area of the property
            area = listing.css('span.css-1cyxwvy.ei6hyam2:nth-child(3)::text').get()
            item['area'] = area.strip().split()[0] if area else 'no info'

            # Extract the number of rooms in the property
            #rooms = listing.css('span.css-cyxwvy.ei6hyam2:nth-child(3)::text').get()
            #item['rooms'] = rooms.strip().split()[0] if rooms else 'no info'

            # Extract the listing link
            listing_link = listing.css('a[data-cy="listing-item-link"]::attr(href)').get()
            item['link1'] = listing_link
            if listing_link:
                # Follow the link to the individual listing page and pass it to a separate method
                yield response.follow(listing_link, callback=self.parse_listing_page)

            # Handle pagination if next page is available
            next_page = response.css('a[data-cy="pagination.next-page"]::attr(href)').get()
            if next_page:
                yield response.follow(next_page, callback=self.parse)

            yield item

    def parse_listing_page(self, response):
        # This method is called for each individual listing page
        listing_info = RentListingItems()

        # Extract information from the individual listing page
        #info_table = response.css('div.css-xr7ajr e10umaf20')
        table_divs = response.css('div.css-kkaknb.enb64yk0')

        try:
            #listing_info['area'] = table_divs[0].css('div::text')[3].get().strip()
            listing_info['area'] = table_divs[0].css('div.css-1wi2w6s.enb64yk4::text').get().strip()
        except:
            listing_info['area'] = 'N/A'

        try:
            listing_info['fees'] = table_divs[1].css('div.css-1wi2w6s.enb64yk4::text').get().strip()
        except:
            listing_info['fees'] = 'N/A'

        try:
            listing_info['rooms_No'] = table_divs[2].css('div.css-1wi2w6s.enb64yk4::text').get().strip()
        except:
            listing_info['rooms_No'] = 'N/A'

        try:
            listing_info['deposit'] = table_divs[3].css('div.css-1wi2w6s.enb64yk4::text').get().strip()
        except:
            listing_info['deposit'] = 'N/A'

        try:
            listing_info['floor'] = table_divs[4].css('div.css-1wi2w6s.enb64yk4::text').get().strip()
        except:
            listing_info['floor'] = 'N/A'

        try:
            listing_info['building_type'] = table_divs[5].css('div.css-1wi2w6s.enb64yk4::text').get().strip()
        except:
            listing_info['building_type'] = 'N/A'
            
        try:
            listing_info['available_from'] = table_divs[6].css('div.css-1wi2w6s.enb64yk4::text').get().strip()
        except:
            listing_info['building_type'] = 'N/A'
            
        try:
            listing_info['balcony'] = table_divs[7].css('div.css-1wi2w6s.enb64yk4::text').get().strip()
        except:
            listing_info['balcony'] = 'N/A'
            
        try:
            listing_info['remote_service'] = table_divs[8].css('div.css-1wi2w6s.enb64yk4::text').get().strip()
        except:
            listing_info['remote_service'] = 'N/A'
            
        try:
            listing_info['interior_state'] = table_divs[6].css('div.css-1wi2w6s.enb64yk4::text').get().strip()
        except:
            listing_info['interior_state'] = 'N/A'    

        try:
            description_div = response.css('div[data-cy="adPageAdDescription"] p::text').getall()
            description = ' '.join(description_div).strip()
            listing_info['description'] = description
        except:
            listing_info['description'] = 'N/A'


        try:
            listing_info['link2'] = response.request.url
        except:
            listing_info['link2'] = 'N/A'
            
        # create a uniqe ID of each listing
        listing_info['listing_ID'] = self.url_to_unique_id(response.request.url)
            
        yield listing_info

    def handle_httperror(self, failure):
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error(f'HTTP Error on {response.url}')
        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error(f'DNS Lookup Error on {request.url}')
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error(f'Timeout Error on {request.url}')