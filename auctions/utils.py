def is_watchlist(request, listing_id):
    return request.user.watchlist.filter(pk=listing_id).exists()

def is_owner(request, listing):
    listing = get_object_or_404(Listing, pk=listing_id)
    return True if request.user.id == listing.seller.id else False