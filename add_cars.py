import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_rental_project.settings')
django.setup()

from rentals.models import Car

cars_data = [
    {"name": "Toyota Corolla", "capacity": 5, "price_per_day": 45.00, "image_url": "https://images.unsplash.com/photo-1590362891991-f776e747a588?auto=format&fit=crop&q=80&w=400"},
    {"name": "Honda Civic", "capacity": 5, "price_per_day": 50.00, "image_url": "https://images.unsplash.com/photo-1606016159991-dfe4f2746ad5?auto=format&fit=crop&q=80&w=400"},
    {"name": "Ford Mustang", "capacity": 4, "price_per_day": 95.00, "image_url": "https://images.unsplash.com/photo-1584345611124-277155d81ea1?auto=format&fit=crop&q=80&w=400"},
    {"name": "Toyota Sienna", "capacity": 7, "price_per_day": 75.00, "image_url": "https://images.unsplash.com/photo-1609521263047-f8f205293f24?auto=format&fit=crop&q=80&w=400"},
    {"name": "Jeep Wrangler", "capacity": 4, "price_per_day": 85.00, "image_url": "https://images.unsplash.com/photo-1559404283-7d722c81373c?auto=format&fit=crop&q=80&w=400"}
]

for data in cars_data:
    Car.objects.get_or_create(**data)
print("Added cars successfully!")
