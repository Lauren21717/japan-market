from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'user_purchases')

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_town_or_city': 'Town or City',
            'default_county': 'County, State or Locality',
            'default_postcode': 'Postal Code',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'profile-form-input'
            self.fields[field].label = False


class UserNameUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'profile-form-input',
            'placeholder': 'Username'
        })


class CustomerPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your current password'
        })

        self.fields['new_password1'].widget.attrs.update({
            'class': 'profile-form-input',
            'placeholder': 'New Password'
        })

        self.fields['new_password2'].widget.attrs.update({
            'class': 'profile-form-input',
            'placeholder': 'Confirm New Password'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password1')
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user
