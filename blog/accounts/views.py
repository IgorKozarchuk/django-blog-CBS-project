from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


# Create your views here.
class SignUpView(CreateView):
	form_class = UserCreationForm
	success_url = reverse_lazy("login")
	template_name = "registration/signup.html"


# NOTE: Why use reverse_lazy here instead of reverse? The reason is that for all generic class-based views the URLs are not loaded when the file is imported, so we have to use the lazy form of reverse to load them later when they’re available.
