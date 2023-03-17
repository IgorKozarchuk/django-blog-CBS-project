from django.urls import path

from . import views


urlpatterns = [
	path("", views.BlogListView.as_view(), name="index"),
	path("post/<int:pk>/", views.BlogDetailView.as_view(), name="post_detail"),
	path('tag/<slug:slug>/', views.tagged, name="tagged"),
	path("post/new/", views.BlogCreateView.as_view(), name="new_post"),
	path("post/<int:pk>/edit/", views.BlogUpdateView.as_view(), name="edit_post"),
	path("post/<int:pk>/delete/", views.BlogDeleteView.as_view(), name="delete_post"),
	path("search/", views.SearchResultsView.as_view(), name="search_results"),
]
