from django.urls import path

from . import views


urlpatterns = [
	path("", views.BlogListView.as_view(), name="index"),
	path("post/<int:pk>/", views.BlogDetailView.as_view(), name="post_detail"),
	path('tag/<slug:slug>/', views.tagged, name="tagged"),
	path("post/new/", views.BlogCreateView.as_view(), name="new_post"),
]
