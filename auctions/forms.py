from django import forms

from .models import Listing, Bid, Comment, Category

class ListingForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Choose one category",
        required=False,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Listing
        fields = [
            "title",
            "category",
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

class CommentingForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "message"
        ]
        labels = {
            "message": "Write something:"
        }
        widgets = {
            "message": forms.Textarea(attrs={
                "class": "form-control"
            })
        }