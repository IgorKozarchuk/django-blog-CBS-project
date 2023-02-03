from django.urls import path

from . import views


urlpatterns = [
	path("", views.BlogListView.as_view(), name="index"),
	path("post/<int:pk>/", views.BlogDetailView.as_view(), name="post_detail"),
]
