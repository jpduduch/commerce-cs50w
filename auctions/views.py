from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import User, Listing, Comment
from .forms import ListingForm, BiddingForm


def index(request):
    
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all().order_by('-creation_date')
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        
        if not form.is_valid():
            return render(request, "auctions/create_listing.html", {
                "form": form
            })
        
        listing = form.save(commit=False)
        listing.seller = request.user
        listing.save()
        return redirect("index")
    
    else:
        form = ListingForm()

    return render(request, "auctions/create_listing.html", {
        "form": form
    })


def listing(request, listing_id, ):
    
    listing = get_object_or_404(Listing, pk=listing_id)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "form": BiddingForm()
    })


@require_POST
def place_bid(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if not request.user.is_authenticated:
        return redirect("login")
        
    form = BiddingForm(request.POST)

    if not form.is_valid():
        request.session["bid_form_error"] = form
        # return render(request, "auctions/listing.html", {
        #     "listing": listing,
        #     "form": form
        # })
    
    if form.cleaned_data["value"] <= listing.current_price:
        request.session["bid_form_error"] = "Bid must be higher than current price."
        return redirect("listing", listing_id=listing_id)
    
    bid = form.save(commit=False)
    bid.bidder = request.user
    bid.listing = listing
    bid.save()
    return redirect("listing", listing_id=listing_id)