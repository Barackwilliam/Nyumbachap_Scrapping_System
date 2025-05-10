from django.urls import path
from .views import *

urlpatterns = [
    path('listings/', listings_view, name='listings'),
    path('', beforward_listings_view, name='beforward_listings'),

]
