from django.shortcuts import render

# Create your views here.
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import MakaziListing

def listings_view(request):
    # Fetch listings from the database
    listings = MakaziListing.objects.all().order_by('-scraped_at')

    # Optionally handle filtering logic
    location = request.GET.get('location', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    # Filtering logic based on GET parameters
    if location:
        listings = listings.filter(location__icontains=location)
    
    def parse_price(price_str):
        try:
            return int(''.join(filter(str.isdigit, price_str)))
        except:
            return 0

    if min_price:
        min_price_val = int(min_price)
        listings = [l for l in listings if parse_price(l.price) >= min_price_val]

    if max_price:
        max_price_val = int(max_price)
        listings = [l for l in listings if parse_price(l.price) <= max_price_val]

    # Create context for the template
    context = {
        'listings': listings,
        'location': location,
        'min_price': min_price,
        'max_price': max_price
    }

    # Return the render response with the context
    return render(request, 'scraper/listings.html', context)




from .models import BeforwardListing

def beforward_listings_view(request):
    listings = BeforwardListing.objects.all().order_by('-scraped_at')
    return render(request, 'scraper/beforward_listings.html', {'listings': listings})
