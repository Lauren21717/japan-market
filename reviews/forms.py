from django import forms
from .models import ProductReview


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f"{i} Starts") for i in range(1, 6)]),  # noqa
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here...'}),  # noqa
        }
