from django.shortcuts import redirect
from .forms import BiddingForm

def handle_bid(request, listing):
    
    form = BiddingForm(request.POST)

    if not form.is_valid():
        return form
    
    if form.cleaned_data["value"] <= listing.current_price:
        form.add_error("value", "Bid must be higher than current price.")
        return form

    return form