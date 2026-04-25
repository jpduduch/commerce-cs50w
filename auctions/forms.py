from django import forms

from .models import Listing, Bid

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            "title",
            "description",
            "starting_price",
            "thumbnail"
        ]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control"
            }),
            "starting_price": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            "thumbnail": forms.ClearableFileInput(attrs={
                "class": "form-control"
            })
        }

class BiddingForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = [
            "value"
        ]
        labels = {
            "value": ""
        }
        widgets = {
            "value": forms.NumberInput(attrs={
                "class": "form-control"
            })
        }