from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Post, Comment
from .forms import CommentForm


# Create your tests here.
class BlogTests(TestCase):
	@classmethod
	def setUpTestData(cls) -> None:
		cls.user = get_user_model().objects.create_user(
			username="testuser",
			email="test@email.com",
			password="1234"
		)
		cls.post = Post.objects.create(
			title="Test title",
			author=cls.user,
			text="Test text"
		)

	def test_post_model(self):
		self.assertEqual(self.post.title, "Test title")
		self.assertEqual(self.post.author.username, "testuser")
		self.assertEqual(self.post.text, "Test text")
		# self.assertEqual(self.post.date.strftime("%d.%m.%Y %H:%M"), "04.02.2023 12:26") # NOTE: change to current date and time
		self.assertEqual(str(self.post), "Test title")
		self.assertEqual(self.post.get_absolute_url(), "/blog_app/post/1/")

	def test_url_exists_at_correct_location_listview(self):
		response = self.client.get("/blog_app/")
		self.assertEqual(response.status_code, 200)

	def test_url_exists_at_correct_location_detailview(self):
		response = self.client.get("/blog_app/post/1/")
		self.assertEqual(response.status_code, 200)

	def test_post_listview(self):
		response = self.client.get(reverse("index"))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Test text")
		self.assertTemplateUsed(response, "blog_app/index.html")

	def test_post_detailview(self):
		response = self.client.get(reverse("post_detail", kwargs={"pk": self.post.pk}))
		no_response = self.client.get('/blog_app/post/9999999/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(no_response.status_code, 404)
		self.assertContains(response, "Test title")
		self.assertTemplateUsed(response, "blog_app/post.html")

	def test_post_createview(self):
		# NOTE: add this line if user needs to be logged in (for example, when using LoginRequiredMixin in create view)
		self.client.force_login(self.user) # https://stackoverflow.com/questions/46001747/django-test-client-post-data
		response = self.client.post(
			reverse("new_post"), {
				"title": "New title",
				"author": self.user.id,
				"text": "New text",
				"tags": "tag1, tag2"
			}
		)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(Post.objects.last().title, "New title")
		self.assertEqual(Post.objects.last().text, "New text")

	def test_post_udateview(self):
		# NOTE: add this line if user needs to be logged in (for example, when using LoginRequiredMixin in create view)
		self.client.force_login(self.user)
		response = self.client.post(
			reverse("edit_post", args="1"), {
				"title": "Updated title",
				"text": "Updated text",
				"tags": "updatedtag1, updatedtag2"
			}
		)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(Post.objects.last().title, "Updated title")
		self.assertEqual(Post.objects.last().text, "Updated text")

	def test_post_deleteview(self):
		response = self.client.post(reverse("delete_post", args="1"))
		self.assertEqual(response.status_code, 302)


class CommentTests(TestCase):
	@classmethod
	def setUpTestData(cls) -> None:
		cls.user = get_user_model().objects.create_user(
			username="testuser",
			email="test@email.com",
			password="1234"
		)
		cls.post = Post.objects.create(
			title="Test title",
			author=cls.user,
			text="Test text"
		)
		cls.comment = Comment.objects.create(
			post=cls.post,
			author=cls.user,
			comment="Test comment"
		)
	
	def test_comment_model(self):
		self.assertEqual(str(self.comment.post), "Test title")
		self.assertEqual(self.comment.author.username, "testuser")
		self.assertEqual(self.comment.comment, "Test comment")
		# self.assertEqual(self.comment.date.strftime("%d.%m.%Y %H:%M"), "12.02.2023 14:07") # NOTE: change to current date and time
		self.assertEqual(self.comment.get_absolute_url(), "/blog_app/post/1/")

	def test_comment_form_valid(self):
		form = CommentForm(data=self.comment.__dict__)
		self.assertTrue(form.is_valid())
