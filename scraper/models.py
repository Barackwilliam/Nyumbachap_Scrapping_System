
# Create your models here.
from django.db import models

class MakaziListing(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField(unique=True)
    price = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    main_image_url = models.URLField(blank=True, null=True)  # New field for the image URL

    scraped_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title




class ScrapeRequest(models.Model):
    url = models.URLField()
    scraped_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url







from django.db import models

class BeforwardListing(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField(unique=True)
    price = models.CharField(max_length=100)
    city = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    agent_name = models.CharField(max_length=255, blank=True)
    agent_phones = models.JSONField(blank=True, null=True)
    image_urls = models.JSONField(blank=True, null=True)
    scraped_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class BeforwardScrapeRequest(models.Model):
    url = models.URLField()
    scraped_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url
