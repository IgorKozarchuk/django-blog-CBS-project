from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager


# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=200)
	author = models.ForeignKey("auth.user", on_delete=models.CASCADE) # many-to-one relationship
	date = models.DateTimeField(auto_now_add=True)
	text = models.TextField()
	img = models.ImageField(upload_to="images/", blank=True)
	# slug = models.SlugField(unique=True, max_length=100, null=True)
	slug = models.SlugField(unique=True, max_length=100, null=False, default="")
	tags = TaggableManager()
	favourites = models.ManyToManyField("auth.user", related_name="favourite", blank=True, default=None)

	def __str__(self) -> str:
		return self.title
	
	def get_absolute_url(self):
		return reverse("post_detail", kwargs={"pk": self.pk})

# How to add to favourites:
# https://www.youtube.com/watch?v=H4QPHLmsZMU


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	author = models.ForeignKey("auth.user", on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)
	comment = models.TextField()

	def __str__(self) -> str:
		return self.comment

	def get_absolute_url(self):
		return reverse("post_detail", kwargs={"pk": self.post.pk})


# How to add tags:
# https://dev.to/thepylot/how-to-add-tags-to-your-models-in-django-django-packages-series-1-3704
# https://www.geeksforgeeks.org/adding-tags-using-django-taggit-in-django-project/
