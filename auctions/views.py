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
    form_bid = BiddingForm()
    comments = Comment.objects.filter(listing=listing_id).order_by("-date")
    form_comments = CommentingForm()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "form_bid": form_bid,
        "comments": comments,
        "form_comment": form_comments

    })


def place_bid(request, listing_id):

    if not request.method == "POST":
        return redirect("listing", listing_id=listing_id)

    if not request.user.is_authenticated:
        return redirect("login")
    
    listing = get_object_or_404(Listing, pk=listing_id)
    form_bid = BiddingForm(request.POST)
    comments = Comment.objects.filter(listing=listing_id).order_by("-date")
    form_comments = CommentingForm()

    if not form_bid.is_valid():
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "form_bid": form_bid,
            "comments": comments,
            "form_comment": form_comments
        })
    
    if form_bid.cleaned_data["value"] <= listing.current_price:
        form_bid.add_error("value", "Bid must be higher than current price.")
        return render(request, "auctions/listing.html", {
           "listing": listing,
            "form_bid": form_bid,
            "comments": comments,
            "form_comment": form_comments
        })
    
    bid = form_bid.save(commit=False)
    bid.bidder = request.user
    bid.listing = listing
    bid.save()

    return redirect("listing", listing_id=listing_id)


def post_comment(request, listing_id):

    if not request.method == "POST":
        return redirect("listing", listing_id=listing_id)
    
    if not request.user.is_authenticated:
        return redirect("login")
    
    form_comment = CommentingForm(request.POST)
    listing = get_object_or_404(Listing, pk=listing_id)
    form_bid = BiddingForm()
    comments = Comment.objects.filter(listing=listing_id).order_by("-date")
    
    if not form_comment.is_valid():
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "form_bid": form_bid,
            "form_comment": form_comment,
            "comments": comments
        })

    comment = form_comment.save(commit=False)
    comment.author = request.user
    comment.listing = listing
    comment.save()
    
    return redirect("listing", listing_id=listing_id)
