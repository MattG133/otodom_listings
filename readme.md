# Otodom Scraping Project

## Description
The project is a Scrapy scraper that downloads data on apartment listings (both for sale and rent) from the most popular real estate website in Poland: otodom.pl. After downloading, the data is cleaned and structured properly and saved to .csv files. The capability of downloading images of the listings is also present, although it's not yet fully developed.

## Table of Contents

- [scrape listings (folder)](#scrape-listings-folder)
  - [data](#data)
    - [raw](#raw) - folder for raw data directly scraped from the website
    - [clean](#clean) - folder for 'clean' data, processed by the data_pipe.py and rent_data_pipe.py scripts
    - [images](#images) - folder for downloaded images
  - [spiders](#spiders)
    - [image_spider.py](#image_spiderpy) - spider for downloading images specifically
    - [listings_spider.py](#listings_spiderpy) - spider for downloading data on sale listings
    - [rent_listings_spider.py](#rent_listings_spiderpy) - spider for downloading data on rent listings
  - [data_pipe.py](#data_pipepy) - cleaning/structuring script for sale data
  - [rent_data_pipe.py](#rent_data_pipepy) - cleaning/structuring script for rent data
  - [items.py](#itemspy) - item descriptions
  - [pipelines.py](#pipelinespy) - pipeline descriptions
  - [settings.py](#settingspy) - Scrapy settings descriptions
  - [middlewares.py](#middlewarespy) - middleware descriptions

## Usage

For downloading sale data:

- In the terminal, run: `scrapy crawl listings` - this script will download all of the sale listings available.
- In the terminal, run: `python3 data_pipe.py` - this script will process raw data and save it to `data/clean`.

For downloading rent data:

- In the terminal, run: `scrapy crawl rent_listings` - this script will download all of the rent listings available.
- In the terminal, run: `python3 rent_data_pipe.py` - this script will process raw data and save it to `data/clean`.

For downloading images:

- In the terminal, run: `scrapy crawl images` - this script will download images of all the sale listings and save them to `data/images`.

## Authors
- MattG133
