from .models import User

def is_watchlist(request, listing_id):
    return request.user.watchlist.filter(pk=listing_id).exists()