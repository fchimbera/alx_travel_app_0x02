from django.urls import path
from .views import (
    ListingListCreate,
    ListingRetrieveUpdateDestroy,
    BookingListCreate,
    BookingRetrieveUpdateDestroy,
    ReviewListCreate,
    ReviewRetrieveUpdateDestroy,
)

urlpatterns = [
    path('listings/', ListingListCreate.as_view(), name='listing-list'),
    path('listings/<int:listng_id>/', ListingRetrieveUpdateDestroy.as_view(), name='listing-detail'),
    path('bookings/', BookingListCreate.as_view(), name='booking-list'),
    path('bookings/<int:booking_id>/', BookingRetrieveUpdateDestroy.as_view(), name='booking-detail'),
    path('reviews/', ReviewListCreate.as_view(), name='review-list'),
    path('reviews/<int:listing_id>/', ReviewRetrieveUpdateDestroy.as_view(), name='review-detail'),
]