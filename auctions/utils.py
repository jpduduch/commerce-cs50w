def is_watchlist(request, listing_id):
    return request.user.watchlist.filter(pk=listing_id).exists() if request.user.is_authenticated else False

def is_owner(request, listing):
    return True if request.user.id == listing.seller.id else False