from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from taggit.models import Tag

from .models import Post
from .forms import CommentForm


# Create your views here.

# constants
ITEMS_PER_PAGE = 5 # max number of items to include on a page when pagintaion is used


class BlogListView(ListView):
	# https://docs.djangoproject.com/en/4.1/topics/pagination/#paginating-a-listview
	paginate_by = ITEMS_PER_PAGE # how many objects should be displayed per page
	model = Post
	template_name = "blog_app/index.html"
	ordering = ["-date"] # sort by date in descending order (new posts on top)


class CommentGet(DetailView):
	model = Post
	template_name = "blog_app/post.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["form"] = CommentForm()
		return context


class CommentPost(SingleObjectMixin, FormView):
	model = Post
	form_class = CommentForm
	template_name = "blog_app/post.html"

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		return super().post(request, *args, **kwargs)

	def form_valid(self, form):
		comment = form.save(commit=False)
		comment.post = self.object
		form.instance.author = self.request.user
		comment.save()
		return super().form_valid(form)

	def get_success_url(self):
		post = self.get_object()
		return reverse("post_detail", kwargs={"pk": post.pk})


# wrapper view, handles GET and POST requests
# class BlogDetailView(LoginRequiredMixin, View):
class BlogDetailView(View):
	def get(self, request, *args, **kwargs):
		view = CommentGet.as_view()
		return view(request, *args, **kwargs)
	
	def post(self, request, *args, **kwargs):
		view = CommentPost.as_view()
		return view(request, *args, **kwargs)


def tagged(request, slug):
	tag = get_object_or_404(Tag, slug=slug)
	posts = Post.objects.filter(tags=tag)
	# https://docs.djangoproject.com/en/4.1/topics/pagination/#using-paginator-in-a-view-function
	paginator = Paginator(posts, ITEMS_PER_PAGE)
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)
	context = {
		"tag": tag,
		"post_list": posts,
		"page_obj": page_obj
	}
	return render(request, "blog_app/index.html", context)


class BlogCreateView(LoginRequiredMixin, CreateView):
	model = Post
	template_name = "blog_app/new_post.html"
	# fields = ["title", "author", "text", "img", "tags"] # show author dropdown
	fields = ["title", "text", "img", "tags"]

	def form_valid(self, form):
		form.instance.slug = slugify(form.instance.title)
		form.instance.author = self.request.user
		return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	template_name = "blog_app/edit_post.html"
	fields = ["title", "text", "img", "tags"]

	def test_func(self):
		obj = self.get_object() # current object returned by the view
		return obj.author == self.request.user # author is a logged in user


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


# Search:
# https://stackoverflow.com/questions/66386490/making-search-bar-in-django
# https://learndjango.com/tutorials/django-search-tutorial
class SearchResultsView(ListView):
	"""Search by post's title and text"""

	paginate_by = ITEMS_PER_PAGE
	model = Post
	template_name = "blog_app/index.html"
	
	def get_queryset(self):
		query = self.request.GET.get("q")
		if query: # if query is not empty
			object_list = Post.objects.filter(
				Q(title__icontains=query) | Q(text__icontains=query)
			)
			return object_list
		return [] # if query is empty, return empty list
