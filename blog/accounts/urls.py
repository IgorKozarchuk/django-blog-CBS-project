from django.urls import path

from . import views


urlpatterns = [
	path("signup/", views.SignUpView.as_view(), name="signup"),
	path("profile/<str:username>/", views.UserProfilelView.as_view(), name="profile"),
	path("fav/<int:pk>/", views.favourite_add, name="favourite_add"),
	path("profile/<str:username>/favourites/", views.favourite_list, name="favourite_list"),
]
