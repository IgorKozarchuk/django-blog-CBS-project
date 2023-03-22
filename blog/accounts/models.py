from django.db import models
# from blog_app.models import Post


# Create your models here.

# https://www.pythontutorial.net/django-tutorial/django-user-profile/
# https://www.devhandbook.com/django/user-profile/
# https://ordinarycoders.com/django-custom-user-profile
# https://dev.to/earthcomfy/django-user-profile-3hik
# https://pylessons.com/django-user-profile

class Profile(models.Model):
	user = models.OneToOneField("auth.user", on_delete=models.CASCADE, related_name="profile")
	email = models.EmailField(blank=True)
	birthday = models.DateField(blank=True, null=True)

	def __str__(self) -> str:
		return self.user.username
	
	# def save(self, *args, **kwargs):
	# 	super().save(*args, **kwargs)
