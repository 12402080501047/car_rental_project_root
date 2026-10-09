from django.core.management.base import BaseCommand
from rentals.models import Car


class Command(BaseCommand):
    help = "Adds a few sample cars so you can test searching and booking right away."

    SAMPLE = [
        ("Maruti Suzuki Swift", 5, 1800),
        ("Hyundai Creta", 5, 2800),
        ("Toyota Innova Crysta", 7, 3500),
        ("Mahindra Scorpio", 7, 3200),
        ("Tata Nexon", 5, 2200),
        ("Force Traveller", 12, 6000),
    ]

    def handle(self, *args, **options):
        created = 0
        for name, capacity, price in self.SAMPLE:
            _, was_created = Car.objects.get_or_create(
                name=name, defaults={"capacity": capacity, "price_per_day": price}
            )
            created += int(was_created)
        self.stdout.write(self.style.SUCCESS(
            f"{created} sample car(s) added. Add image URLs from the admin panel."
        ))
