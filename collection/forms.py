from django import forms
from .models import Category, Product, ProductType, ShopByOption


class ProfuctForm(forms.ModelForm):

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

        self.fields['product_type'] = forms.ModelMultipleChoiceField(
            queryset=types,
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )
        self.fields['product_type'].choices = [
            (t.id, t.get_friendly_name()) for t in types
        ]

        self.fields['shop_by_option'] = forms.ModelMultipleChoiceField(
            queryset=options,
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )
        self.fields['shop_by_option'].choices = [
            (o.id, o.get_friendly_name()) for o in options
        ]

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'

