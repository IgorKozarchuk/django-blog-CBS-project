from django.db import models

# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=200)
	author = models.ForeignKey("auth.user", on_delete=models.CASCADE) # many-to-one relationship
	date = models.DateTimeField(auto_now_add=True)
	text = models.TextField()

	def __str__(self) -> str:
		return self.title
