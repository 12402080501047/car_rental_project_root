from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Car(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    image_url = models.URLField(max_length=200, blank=True, null=True)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.car.name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    license_number = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # get_or_create keeps this safe for users that existed before Profile did
    profile, _ = Profile.objects.get_or_create(user=instance)
    profile.save()
