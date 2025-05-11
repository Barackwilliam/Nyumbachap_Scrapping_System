from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BeforwardListing
import requests

API_URL = 'https://base.nyumbachap.com/api/receive-beforward-listing/'
API_HEADERS = {
    'Authorization': 'Token 7d9a3f905bf0c9fa46147447226d966d82f2ddf6',
    'Content-Type': 'application/json',
}

@receiver(post_save, sender=BeforwardListing)
def send_beforward_listing_to_nyumbachap(sender, instance, created, **kwargs):
    data = {
        'title': instance.title,
        'link': instance.link,
        'price': instance.price,
        'city': instance.city,
        'description': instance.description,
        'agent_name': instance.agent_name,
        'agent_phones': instance.agent_phones,
        'image_urls': instance.image_urls,
        'scraped_at': instance.scraped_at.isoformat(),
    }
    try:
        response = requests.post(API_URL, json=data, headers=API_HEADERS)
        response.raise_for_status()
        print(f'Successfully sent Beforward listing: {instance.title}')
    except requests.RequestException as e:
        print(f'Failed to send Beforward listing: {instance.title} - {e}')
