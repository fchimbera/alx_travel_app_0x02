from django.db import models
from django.utils import timezone

class Listing(models.Model):
    listng_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class Booking(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    booking_id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=100)  # Assuming a simple string for user; replace with User model if needed
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Booking for {self.listing.title} by {self.user}"

class Review(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    user = models.CharField(max_length=100)  # Assuming a simple string for user; replace with User model if needed
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Review for {self.listing.title} by {self.user}"
