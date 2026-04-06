from django import forms

from .models import Listing

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
    