# import asyncio
# from django.core.management.base import BaseCommand
# from scraper.models import RentalListing
# from asgiref.sync import sync_to_async
# from playwright.async_api import async_playwright
# import logging

# # Set up logging for debugging
# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)

# class Command(BaseCommand):
#     help = 'Scrape rental listings using Playwright'

#     def handle(self, *args, **options):
#         try:
#             asyncio.run(self.scrape())
#             self.stdout.write(self.style.SUCCESS('Scraping completed and data saved.'))
#         except Exception as e:
#             logger.error(f"Error during scraping: {str(e)}")
#             self.stdout.write(self.style.ERROR(f'Error occurred: {str(e)}'))

#     async def scrape(self):
#         async with async_playwright() as p:
#             try:
#                 browser = await p.chromium.launch(headless=True)
#                 page = await browser.new_page()

#                 url = "https://makazimapya.com/listings/nyumbaapartment-ya-vyumba-viwili-inapangishwa-ubungo-dar-es-salaam/d9614526-7970-4865-87c0-0d1437e24efa"  # Replace with actual URL of listings
#                 await page.goto(url)

#                 # Wait for the page to load
#                 await page.wait_for_selector(".listing", timeout=10000)  # Update the timeout if necessary
#                 listings = await page.query_selector_all(".listing")  # Update selector if needed

#                 # Check if any listings are found
#                 if not listings:
#                     self.stdout.write(self.style.WARNING('No listings found. Check your CSS selectors or the page structure.'))

#                 # Loop over each listing and scrape details
#                 for listing in listings:
#                     try:
#                         title = await listing.query_selector_eval(".title", "el => el.innerText")  # Update selector
#                         price = await listing.query_selector_eval(".price", "el => el.innerText")
#                         location = await listing.query_selector_eval(".location", "el => el.innerText")
#                         description = await listing.query_selector_eval(".description", "el => el.innerText")
#                         link = await listing.query_selector_eval("a", "el => el.href")

#                         # Print the scraped data to the console
#                         self.stdout.write(f"Title: {title}")
#                         self.stdout.write(f"Price: {price}")
#                         self.stdout.write(f"Location: {location}")
#                         self.stdout.write(f"Description: {description}")
#                         self.stdout.write(f"Link: {link}")
#                         self.stdout.write("\n---\n")  # Separator for each listing

#                         # Save to the database using sync_to_async
#                         await self.save_listing_to_db(link, title, price, location, description)

#                     except Exception as e:
#                         logger.error(f"Error processing listing: {str(e)}")

#                 await browser.close()

#             except Exception as e:
#                 logger.error(f"Error during scraping session: {str(e)}")
#                 await browser.close()

#     @sync_to_async
#     def save_listing_to_db(self, link, title, price, location, description):
#         # Ensure the RentalListing object is created or updated correctly
#         obj, created = RentalListing.objects.update_or_create(
#             link=link,
#             defaults={
#                 'title': title,
#                 'price': price,
#                 'location': location,
#                 'description': description,
#             }
#         )
#         if created:
#             logger.info(f"Created new listing: {title}")
#         else:
#             logger.info(f"Updated existing listing: {title}")

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from scraper.models import RentalListing  # your Django model

class Command(BaseCommand):
    help = 'Scrape a single Makazi Mapya listing and save to DB'

    def handle(self, *args, **kwargs):
        # url = 'https://makazimapya.com/listings/nyumbaapartment-ya-vyumba-viwili-inapangishwa-ubungo-dar-es-salaam/d9614526-7970-4865-87c0-0d1437e24efa'
        url = 'https://makazimapya.com/listings/nyumba-inapangishwa-sakina-arusha/03fa1eef-e6db-4214-900f-03c66440a28a'
        #url = 'https://makazimapya.com/listings/nyumba-inapangishwa-sakina-arusha/461476bc-88d0-466d-a8bb-cfc7a0a7172c'
        #url = 'https://makazimapya.com/listings/nyumba-inapangishwa-sakina-arusha/bf53c53a-535e-43a3-b016-7c78eee602a7'
        #url = 'https://makazimapya.com/listings/nyumba-inapangishwa-sakina-arusha/03fa1eef-e6db-4214-900f-03c66440a28a'
        #url = 'https://makazimapya.com/listings/nyumbaapartment-ya-chumba-kimoja-inapangishwa-sakina-arusha/fb129c5a-772a-4db5-85cc-8fda06c29b7f'
        # url = ''
        # url = ''
        # url = ''
        # url = ''


        response = requests.get(url)
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f'Failed to fetch page: {response.status_code}'))
            return

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract title
        title_tag = soup.find('h1', class_='text-2xl')
        title = title_tag.get_text(strip=True) if title_tag else 'No title'

        # Extract price
        price_tag = soup.find('span', class_='text-xl font-bold text-green-600')
        price = price_tag.get_text(strip=True) if price_tag else 'No price'

        # Extract location
        location_tag = soup.select_one('a[href*="location"]')
        location = location_tag.get_text(strip=True) if location_tag else 'No location'

        # Extract description
        desc_tag = soup.find('p', class_='text-slate-600')
        description = desc_tag.get_text(separator='\n', strip=True) if desc_tag else ''

        # Extract main image URL
        main_img_tag = soup.find('img', alt='media -1')
        main_image_url = main_img_tag['src'] if main_img_tag else ''

        # Save to database
        obj, created = RentalListing.objects.update_or_create(
            link=url,
            defaults={
                'title': title,
                'price': price,
                'location': location,
                'description': description,
                'main_image_url': main_image_url,
            }
        )
        action = 'Created' if created else 'Updated'
        self.stdout.write(f'{action} listing: {title}')
