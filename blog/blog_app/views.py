from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
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
