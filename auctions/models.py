from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True)

    def __str__(self):
        return self.username
    

class Category(models.Model):
    name = models.CharField(max_length=64)

    @property
    def count(self):
        amount = len(self.items.all())
        return amount

    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=8, decimal_places=2, default=0, validators=[
        MinValueValidator(0)
    ])
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(blank=True, null=True, upload_to="listings/")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="items")

    @property
    def current_price(self):
        highest_bid = self.bids.order_by('-value').first()
        
        return self.starting_price if highest_bid is None else highest_bid.value
    
    def __str__(self):
        return self.title


class Bid(models.Model):
    value = models.DecimalField(max_digits=8, decimal_places=2, default=0,
    validators=[
        MinValueValidator(0)
    ])
    date = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"$ {self.value}"


class Comment(models.Model):
    message = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return self.message