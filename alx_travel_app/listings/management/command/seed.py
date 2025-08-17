from django.core.management.base import BaseCommand
from listings.models import Listing  # Import your Listing model
import random

class Command(BaseCommand):
    help = 'Populates the database with sample listing data.' # This text will be shown when you run 'python manage.py help seed'

    def handle(self, *args, **options):
        # Clear existing listings to prevent duplicates if you run the command multiple times
        Listing.objects.all().delete()
        self.stdout.write(self.style.WARNING('Deleted all existing listings.'))

        # Data for sample listings
        titles = [
            "Cozy Apartment in City Center",
            "Spacious Family Home with Garden",
            "Modern Studio Near Beach",
            "Charming Cottage in the Countryside",
            "Luxury Penthouse with Skyline View"
        ]
        descriptions = [
            "A beautiful and comfortable apartment perfect for short stays.",
            "Plenty of room for a family, with a large private garden.",
            "Sleek and minimalist design, just a few minutes walk to the ocean.",
            "Escape the hustle and bustle in this quaint and peaceful retreat.",
            "Experience urban living at its finest in this high-end residence."
        ]

        # Create 10 sample listings
        for i in range(10):
            title = random.choice(titles)
            description = random.choice(descriptions)
            price = round(random.uniform(50.00, 500.00), 2) # Random price between 50 and 500
            available = random.choice([True, False])

            Listing.objects.create(
                title=title,
                description=description,
                price=price,
                available=available
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created listing: {title}'))

        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample listing data.'))