from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from taggit.models import Tag

from .models import Post
from .forms import CommentForm


# Create your views here.
class BlogListView(ListView):
	model = Post
	template_name = "blog_app/index.html"
	ordering = ["-date"] # sort by date in descending order (new posts on top)


class BlogDetailView(DetailView):
	model = Post
	template_name = "blog_app/post.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["form"] = CommentForm()
		return context


def tagged(request, slug):
	tag = get_object_or_404(Tag, slug=slug)
	posts = Post.objects.filter(tags=tag)
	context = {
		"tag": tag,
		"post_list": posts,
	}
	return render(request, "blog_app/index.html", context)


class BlogCreateView(LoginRequiredMixin, CreateView):
	model = Post
	template_name = "blog_app/new_post.html"
	fields = ["title", "author", "text", "img", "tags"]

	def form_valid(self, form):
		print(form.instance.title)
		form.instance.slug = slugify(form.instance.title)
		return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	template_name = "blog_app/edit_post.html"
	fields = ["title", "text", "img", "tags"]

	def test_func(self):
		obj = self.get_object() # current object returned by the view
		return obj.author == self.request.user # author is logged in user


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	template_name = "blog_app/delete_post.html"
	success_url = reverse_lazy("index")

	def test_func(self):
		obj = self.get_object()
		return obj.author == self.request.user


# NOTE: When using mixins with class-based views the order is important.
# LoginRequiredMixin comes first so that we force log in, then we add UserPassesTestMixin for an additional layer of functionality,
# and finally either UpdateView or DeleteView.
