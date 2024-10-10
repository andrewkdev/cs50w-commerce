from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import User, AuctionListing, Category, Bid, Comment
from django.contrib.auth.decorators import login_required
from .forms import AuctionListingForm
from decimal import Decimal, InvalidOperation
from django.contrib import messages


def index(request):
    # Fetch all active listings
    active_listings = AuctionListing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": active_listings
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
    if request.method == 'POST':
        form = AuctionListingForm(request.POST)
        if form.is_valid():
            # Save the form but don't commit to the database yet
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.current_price = listing.starting_bid
            listing.save()
            return redirect('index')
    else:
        form = AuctionListingForm()
    return render(request, 'auctions/create_listing.html', {
        'form': form
    })

def listing(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    user = request.user
    comments = listing.comments.all()
    highest_bid = listing.bids.order_by("-amount").first()
    bid_count = listing.bids.count()

    if request.method == "POST":
        if "bid" in request.POST:
            try:
                # Convert the bid amount to a Decimal
                bid_amount = Decimal(request.POST["bid"])
                # Validate that it's greater than the current price
                if user.is_authenticated and bid_amount > listing.current_price:
                    new_bid = Bid(amount=bid_amount, bidder=user, auction_listing=listing)
                    new_bid.save()
                    listing.current_price = bid_amount
                    listing.save()
                    messages.success(request, "Your bid was placed successfully.")
                    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
                else:
                    messages.error(request, "Your bid must be higher than the current price.")
            except (InvalidOperation, ValueError):
                # Handle invalid bid input
                messages.error(request, "Invalid bid amount. Please enter a valid number.")

        elif "comment" in request.POST:
            content = request.POST["comment"]
            new_comment = Comment(user=user, listing=listing, content=content)
            new_comment.save()
            messages.success(request, "Your comment has been posted.")
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

        elif "close" in request.POST:
            if user == listing.owner:
                listing.is_active = False
                listing.save()
                messages.success(request, "The auction has been closed.")
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    is_in_watchlist = user.is_authenticated and user in listing.watchlist.all()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_in_watchlist": is_in_watchlist,
        "comments": comments,
        "highest_bid": highest_bid,
        "bid_count": bid_count
    })


def toggle_watchlist(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    user = request.user

    if user.is_authenticated:
        if user in listing.watchlist.all():
            listing.watchlist.remove(user)
            messages.success(request, "Listing removed from your watchlist.")
        else:
            listing.watchlist.add(user)
            messages.success(request, "Listing added to your watchlist.")
    else:
        messages.error(request, "You need to log in to manage your watchlist.")

    return redirect("listing", listing_id=listing_id)

# In views.py
def watchlist(request):
    user = request.user
    watchlist_items = AuctionListing.objects.filter(watchlist=user)  # Assuming 'watchlist' is a ManyToMany field in your model
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist_items
    })

def categories(request):
    categories_list = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories_list
    })

def category_listings(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    listings_in_category = category.listings.filter(is_active=True)
    return render(request, "auctions/category_listings.html", {
        "category": category,
        "listings": listings_in_category
    })