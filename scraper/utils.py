# scraper/utils.py (create this file)

import requests
from bs4 import BeautifulSoup
from .models import MakaziListing

def scrape_and_save_listing(url):
    response = requests.get(url)
    if response.status_code != 200:
        return f"Failed to fetch page: {response.status_code}"

    soup = BeautifulSoup(response.content, 'html.parser')

    title_tag = soup.find('h1', class_='text-2xl')
    title = title_tag.get_text(strip=True) if title_tag else 'No title'

    price_tag = soup.find('span', class_='text-xl font-bold text-green-600')
    price = price_tag.get_text(strip=True) if price_tag else 'No price'

    location_tag = soup.select_one('a[href*="location"]')
    location = location_tag.get_text(strip=True) if location_tag else 'No location'

    desc_tag = soup.find('p', class_='text-slate-600')
    description = desc_tag.get_text(separator='\n', strip=True) if desc_tag else ''

    main_img_tag = soup.find('img', alt='media -1')
    main_image_url = main_img_tag['src'] if main_img_tag else ''

    obj, created = MakaziListing.objects.update_or_create(
        link=url,
        defaults={
            'title': title,
            'price': price,
            'location': location,
            'description': description,
            'main_image_url': main_image_url,
        }
    )
    return f"{'Created' if created else 'Updated'}: {title}"





from urllib.parse import urljoin  # to join relative URLs with the base URL
from .models import BeforwardListing
def scrape_and_save_beforward_listing(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find('h1').get_text(strip=True)
        price_tag = soup.select_one('li.item-price')
        price = price_tag.get_text(strip=True) if price_tag else 'N/A'
        desc_div = soup.find('div', class_='property-description-content')
        description = desc_div.get_text(separator='\n', strip=True) if desc_div else ''
        city_li = soup.select_one('#property-address-wrap li.detail-city span')
        city = city_li.get_text(strip=True) if city_li else 'N/A'

        agent_name = soup.select_one('.agent-name')
        agent_name = agent_name.get_text(strip=True) if agent_name else 'N/A'
        agent_phones = [a.get_text(strip=True) for a in soup.select('.agent-phone a[href^="tel:"]')]
        
        # Select image URLs and convert relative URLs to absolute URLs
        image_divs = soup.select('#property-gallery-js .lslide img')
        image_urls = [urljoin(url, img['src']) for img in image_divs[:4] if img.get('src')]

        obj, created = BeforwardListing.objects.update_or_create(
            link=url,
            defaults={
                'title': title,
                'price': price,
                'description': description,
                'city': city,
                'agent_name': agent_name,
                'agent_phones': agent_phones,
                'image_urls': image_urls,
            }
        )

        return f"✅ Scraped: {title}" if created else f"🔁 Updated: {title}"

    except Exception as e:
        return f"❌ Failed to scrape {url}: {str(e)}"







# utils.py
import requests

NYUMBACHAP_API_URL = 'https://base.nyumbachap.com/api/receive-scraped/'
NYUMBACHAP_TOKEN = '7d9a3f905bf0c9fa46147447226d966d82f2ddf6'  # Replace na token yako ya kweli

def send_to_nyumbachap(instance):
    data = {
        'title': instance.title,
        'link': instance.link,
        'price': instance.price,
        'location': instance.location,
        'description': instance.description,
        'main_image_url': instance.main_image_url,
    }

    headers = {
        'Authorization': f'Token {NYUMBACHAP_TOKEN}',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.post(NYUMBACHAP_API_URL, json=data, headers=headers)
        print(f"[{response.status_code}] Sent to NyumbaChap: {response.json()}")
    except Exception as e:
        print("Error sending to NyumbaChap:", str(e))
