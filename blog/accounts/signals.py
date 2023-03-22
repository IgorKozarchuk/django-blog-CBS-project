from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


# https://www.pythontutorial.net/django-tutorial/django-user-profile/
# If you log in into account without a profile and access the profile page, you’ll get an error. The reason is that we haven’t created the profile for this user. To fix this issue, we should create a profile once a user registers successfully. To implement this, we’ll use something called signals in Django.

# Creates a new profile after a User object is created
@receiver(post_save, sender="auth.user")
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

# Updates the profile after a User object is saved
@receiver(post_save, sender="auth.user")
def save_profile(sender, instance, **kwargs):
	instance.profile.save()
