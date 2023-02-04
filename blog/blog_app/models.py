from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager


# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=200)
	author = models.ForeignKey("auth.user", on_delete=models.CASCADE) # many-to-one relationship
	date = models.DateTimeField(auto_now_add=True)
	text = models.TextField()
	slug = models.SlugField(unique=True, max_length=100, null=True)
	tags = TaggableManager()

	def __str__(self) -> str:
		return self.title
	
	def get_absolute_url(self):
		return reverse("post_detail", kwargs={"pk": self.pk})


# How to add tags:
# https://dev.to/thepylot/how-to-add-tags-to-your-models-in-django-django-packages-series-1-3704
# https://www.geeksforgeeks.org/adding-tags-using-django-taggit-in-django-project/
