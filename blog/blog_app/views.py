from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from taggit.models import Tag

from .models import Post


# Create your views here.
class BlogListView(ListView):
	model = Post
	template_name = "blog_app/index.html"


class BlogDetailView(DetailView):
	model = Post
	template_name = "blog_app/post.html"


def tagged(request, slug):
	tag = get_object_or_404(Tag, slug=slug)
	posts = Post.objects.filter(tags=tag)
	context = {
		"tag": tag,
		"post_list": posts,
	}

	return render(request, "blog_app/index.html", context)


class BlogCreateView(CreateView):
	model = Post
	template_name = "blog_app/new_post.html"
	fields = ["title", "author", "text", "img", "tags"]

	def form_valid(self, form):
		print(form.instance.title)
		form.instance.slug = slugify(form.instance.title)
		return super().form_valid(form)


class BlogUpdateView(UpdateView):
	model = Post
	template_name = "blog_app/edit_post.html"
	fields = ["title", "text", "img", "tags"]


class BlogDeleteView(DeleteView):
	model = Post
	template_name = "blog_app/delete_post.html"
	success_url = reverse_lazy("index")
