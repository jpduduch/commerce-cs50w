from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import User, Listing, Comment
from .forms import ListingForm, BiddingForm, CommentingForm


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
        
        if form.cleaned_data["category"] == None:
            form.add_error("category", "Please pick a category.")
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

def listing(request, listing_id):

    listing = get_object_or_404(Listing, pk=listing_id)

    # receives a user bid if there is one
    bid_data = request.session.pop("bid_data", None)
    bid_error = request.session.pop("bid_error", None)
    bidding_form = BiddingForm(bid_data) if bid_data else BiddingForm()
    
    # handles the bid data
    if bid_data:
        bidding_form.is_valid()
    if bid_error:
        for field, message in bid_error.items():
            bidding_form.add_error(field, message)

    comments = Comment.objects.filter(listing=listing_id).order_by("-date")
    
    # receives a user comment if there is any
    comment_data = request.session.pop("comment_data", None)
    commenting_form = CommentingForm(comment_data) if comment_data else CommentingForm()

    # handles the comment data
    if comment_data:
        commenting_form.is_valid()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bidding_form": bidding_form,
        "comments": comments,
        "commenting_form": commenting_form
    })


@require_POST
@login_required
def place_bid(request, listing_id):
    
    form = BiddingForm(request.POST)

    if not form.is_valid():
        request.session["bid_data"] = request.POST.dict()
        return redirect("listing", listing_id=listing_id)
    
    listing = get_object_or_404(Listing, pk=listing_id)
    
    if form.cleaned_data["value"] <= listing.current_price:
        request.session["bid_data"] = request.POST.dict()
        request.session["bid_error"] = {"value": "Bid must be higher than current price."}
        return redirect("listing", listing_id=listing_id)
    
    bid = form.save(commit=False)
    bid.listing = listing
    bid.bidder = request.user
    bid.save()

    return redirect("listing", listing_id=listing_id)


@require_POST
@login_required
def post_comment(request, listing_id):
    
    form = CommentingForm(request.POST)
    
    if not form.is_valid():
        request.session["comment_data"] = request.POST.dict()
        return redirect("listing", listing_id=listing_id)
    
    comment = form.save(commit=False)
    comment.author = request.user
    comment.listing = get_object_or_404(Listing, pk=listing_id)
    comment.save()

    return redirect("listing", listing_id=listing_id)
