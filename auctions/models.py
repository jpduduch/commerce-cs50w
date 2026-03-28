from django.contrib.auth.models import AbstractUser
from django.db import models

# handles users
class User(AbstractUser):
    pass

# handles auction listings
class Auction_listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    current_price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField()
    # The default route of your web application should let users view all of the currently active auction listings. For each active listing, this page should display (at minimum) the title, description, current price, and photo (if one exists for the listing).

# handles bids

# handles comments on auction listings
