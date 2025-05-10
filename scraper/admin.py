
# scraper/admin.py

from django.contrib import admin
from .models import MakaziListing, ScrapeRequest
from .utils import scrape_and_save_listing

@admin.register(MakaziListing)
class MakaziListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price', 'scraped_at')

@admin.register(ScrapeRequest)
class ScrapeRequestAdmin(admin.ModelAdmin):
    list_display = ('url', 'scraped_at')
    actions = ['scrape_selected_urls']

    def scrape_selected_urls(self, request, queryset):
        messages = []
        for obj in queryset:
            result = scrape_and_save_listing(obj.url)
            messages.append(result)
        self.message_user(request, "\n".join(messages))

    scrape_selected_urls.short_description = "Scrape selected URLs"








from .models import BeforwardListing, BeforwardScrapeRequest
from .utils import scrape_and_save_beforward_listing

@admin.register(BeforwardListing)
class BeforwardListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'price', 'scraped_at')


@admin.register(BeforwardScrapeRequest)
class BeforwardScrapeRequestAdmin(admin.ModelAdmin):
    list_display = ('url', 'scraped_at')
    actions = ['scrape_selected_urls']

    def scrape_selected_urls(self, request, queryset):
        messages = []
        for obj in queryset:
            result = scrape_and_save_beforward_listing(obj.url)
            messages.append(result)
        self.message_user(request, "\n".join(messages))

    scrape_selected_urls.short_description = "Scrape selected Beforward URLs"