from django.contrib import admin

from .models import User, Listing, Bid, Comment

# Register your models here.
class ListingAdnmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "starting_price", "seller", "thumbnail")

admin.site.register(User)
admin.site.register(Listing, ListingAdnmin)
admin.site.register(Bid)
admin.site.register(Comment)

