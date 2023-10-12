from pathlib import Path
from scrape_listings.pipelines import CsvExportPipeline1, CsvExportPipeline2
from scrape_listings.items import ListingItems, ListingsPage
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
import scrapy

class ListingsSpider(scrapy.Spider):
    name = 'listings'

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrape_listings.middlewares.RotateUserAgentMiddleware': 400,
            # Add other middleware settings if needed
        },
    }

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        start_urls = [
            f'https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa?viewType=listing&page={page}'
            for page in range(1, 301)  # Generate URLs for pages 1 to 300
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response):
        listings = response.css('li[data-cy="listing-item"]')

        for listing in listings:
            item = ListingsPage()
            
            # Extract the title of the listing
            title = listing.css('span[data-cy="listing-item-title"]::text').get()
            item['title'] = title.strip() if title else 'no info'

            # Extract the address of the listing
            address = listing.css('p.css-19dkezj.e1n06ry53::text').get()
            item['address'] = address.strip() if address else 'no info'

            # Extract the price of the listing
            price = listing.css('span.css-1cyxwvy.ei6hyam2::text').get()
            item['price'] = price.strip() if price else 'no info'

            # Extract the area of the property
            area = listing.css('span.css-1cyxwvy.ei6hyam2:nth-child(4)::text').get()
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
        listing_info = ListingItems()

        # Extract information from the individual listing page
        #info_table = response.css('div.css-xr7ajr e10umaf20')
        table_divs = response.css('div.css-kkaknb.enb64yk0')

        try:
            #listing_info['area'] = table_divs[0].css('div::text')[3].get().strip()
            listing_info['ownership_form'] = table_divs[1].css('div.css-1wi2w6s.enb64yk4::text').get().strip()
        except AttributeError:
            listing_info['ownership_form'] = 'N/A'

        try:
            listing_info['rooms_No'] = table_divs[2].css('div.css-1wi2w6s.enb64yk4::text').get().strip()
        except AttributeError:
            listing_info['rooms_No'] = 'N/A'

        try:
            listing_info['interior_state'] = table_divs[3].css('div.css-1wi2w6s.enb64yk4::text').get().strip()
        except AttributeError:
            listing_info['interior_state'] = 'N/A'

        try:
            listing_info['floor'] = table_divs[4].css('div.css-1wi2w6s.enb64yk4::text').get().strip()
        except AttributeError:
            listing_info['floor'] = 'N/A'

        try:
            listing_info['balcony'] = table_divs[5].css('div.css-1wi2w6s.enb64yk4::text').get().strip()
        except AttributeError:
            listing_info['balcony'] = 'N/A'

        try:
            listing_info['parking_space'] = table_divs[7].css('div.css-1wi2w6s.enb64yk4::text').get().strip()
        except AttributeError:
            listing_info['parking_space'] = 'N/A'

        # try:
        #     description_div = response.css('div[data-cy="adPageAdDescription"].css-1wekrze.w1lbnp621::text')
        #     description = ' '.join(description_div.css('p::text').getall()).strip()
        #     listing_info['description'] = description
        # except AttributeError:
        #     listing_info['description'] = 'N/A'

        try:
            listing_info['link2'] = response.request.url
        except AttributeError:
            listing_info['link2'] = 'N/A'

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