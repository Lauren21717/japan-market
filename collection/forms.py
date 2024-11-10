from django import forms
from .models import Category, Product, ProductType, ShopByOption

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        categories = Category.objects.all()
        types = ProductType.objects.all()
        options = ShopByOption.objects.all()
        
        self.fields['category'].choices = [
            (c.id, c.get_friendly_name()) for c in categories
        ]
        
        self.fields['product_type'] = forms.ModelChoiceField(
            queryset=types,
            empty_label="Select a product type",
        )
        
        self.fields['shop_by_option'] = forms.ModelMultipleChoiceField(
            queryset=options,
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )