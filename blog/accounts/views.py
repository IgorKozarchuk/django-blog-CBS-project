from django.views.generic import View, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator

from .forms import ProfileForm
from blog_app.models import Post


# Create your views here.
class SignUpView(CreateView):
	form_class = UserCreationForm
	success_url = reverse_lazy("login")
	template_name = "registration/signup.html"

# NOTE: Why use reverse_lazy here instead of reverse? The reason is that for all generic class-based views the URLs are not loaded when the file is imported, so we have to use the lazy form of reverse to load them later when they’re available.


class UserProfilelView(LoginRequiredMixin, View):
	def get(self, request, username):
		profile_form = ProfileForm(instance=request.user.profile)
		template_name = "accounts/profile.html"
		context = {
			"profile_form": profile_form,
			"username": username,
			"profile": request.user.profile
		}

		return render(request=request, template_name=template_name, context=context)
	
	def post(self, request, username):
		profile_form = ProfileForm(request.POST, instance=request.user.profile)
		template_name = "accounts/profile.html"

		if profile_form.is_valid():
			profile_form.save()
			messages.success(request, "Your profile has been updated")
			return redirect("profile", username=username)
		else:
			messages.error(request, "Error updating your profile")
			context = {
				"profile_form": profile_form,
				"username": username,
				"profile": request.user.profile,
				"messages": messages
			}
			
			return render(request=request, template_name=template_name, context=context)


@login_required
def favourite_add(request, pk):
	post = get_object_or_404(Post, pk=pk)
	# if already added, remove post from favourites
	if post.favourites.filter(pk=request.user.pk).exists():
		post.favourites.remove(request.user)
	else: # add post to favourites otherwise
		post.favourites.add(request.user)
	
	return redirect(request.META.get("HTTP_REFERER", "redirect_if_referer_not_found"))


@login_required
def favourite_list(request, username):
	favor_posts = Post.objects.filter(favourites=request.user).order_by("date")
	template_name = "accounts/favourites.html"
	paginator = Paginator(favor_posts, 10)
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)
	context = {
		# "favor_posts": favor_posts,
		"username": username,
		"page_obj": page_obj
	}

	return render(request=request, template_name=template_name, context=context)
