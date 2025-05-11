from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MakaziListing
import requests

API_URL = 'https://base.nyumbachap.com/api/receive-listing/'
API_HEADERS = {
    'Authorization': 'Token 7d9a3f905bf0c9fa46147447226d966d82f2ddf6',
    'Content-Type': 'application/json',
}

@receiver(post_save, sender=MakaziListing)
def send_listing_to_nyumbachap(sender, instance, created, **kwargs):
    data = {
        'title': instance.title,
        'link': instance.link,
        'price': instance.price,
        'location': instance.location,
        'description': instance.description,
        'main_image_url': instance.main_image_url,
        'scraped_at': instance.scraped_at.isoformat(),
    }
    try:
        response = requests.post(API_URL, json=data, headers=API_HEADERS)
        response.raise_for_status()
        print(f'Successfully sent Makazi listing: {instance.title}')
    except requests.RequestException as e:
        print(f'Failed to send Makazi listing: {instance.title} - {e}')

