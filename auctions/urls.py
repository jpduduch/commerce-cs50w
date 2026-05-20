from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new-listing", views.create_listing, name="create"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("place-bid/<int:listing_id>", views.place_bid, name="place_bid"),
    path("post-comment/<int:listing_id>", views.post_comment, name="post_comment"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category_filter, name="category_filter"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist-manage/<int:listing_id>", views.watchlist_manage, name="watchlist_manage"),
    path("close-auction/<int:listing_id>", views.close_auction, name="close_auction")
]
