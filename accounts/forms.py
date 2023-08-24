from django import forms
from .models import Account,Address
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'company', 'country', 'password']
    
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Password does not match!")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        self.fields['company'].widget.attrs['placeholder'] = 'Enter Company Name'
        self.fields['country'].widget.attrs['placeholder'] = 'Enter Country Name'
 


class UserForm(forms.ModelForm):
  class Meta:
    model = Account
    fields = ['first_name', 'last_name', 'phone_number', 'date_of_birth']



class ChangePasswordForm(PasswordChangeForm):

    class Meta:
        model = User
        fields = '__all__'


class AddressForm(forms.ModelForm):
  class Meta:
    model = Address
    fields = ['email', 'mobile', 'first_name', 'last_name', 'address', 'landmark', 'city', 'pin_code', 'state', 'country']
 