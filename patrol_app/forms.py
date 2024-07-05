from django import forms
from allauth.account.forms import SignupForm
from allauth.account.adapter import DefaultAccountAdapter
from .models import CustomUser

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='姓')
    last_name = forms.CharField(max_length=30, label='名')
    email = forms.CharField(max_length=150, label='メールアドレス')
    telephone_number = forms.CharField(max_length=150, label='電話番号')
    post_code = forms.CharField(max_length=150, label='郵便番号')
    address = forms.CharField(max_length=150, label='住所')
    
    class Meta:
        model = CustomUser

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.telephone_number = self.cleaned_data['telephone_number']
        user.post_code = self.cleaned_data['post_code']
        user.address = self.cleaned_data['address']
        user.save()
        return user