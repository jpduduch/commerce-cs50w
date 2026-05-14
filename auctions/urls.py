from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new-listing", views.create_listing, name="create"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>/bid", views.place_bid, name="place_bid"),
    path("<int:listing_id>/comment", views.post_comment, name="post_comment")
]
