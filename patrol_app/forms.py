from django import forms
from allauth.account.forms import SignupForm
from allauth.account.adapter import DefaultAccountAdapter
from .models import CustomUser, Review

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

class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='姓')
    last_name = forms.CharField(max_length=30, label='名')
    email = forms.CharField(max_length=150, label='メールアドレス')
    telephone_number = forms.CharField(max_length=150, label='電話番号')
    post_code = forms.CharField(max_length=150, label='郵便番号')
    address = forms.CharField(max_length=150, label='住所')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'image']

class ReviewSearchForm(forms.Form):
    query = forms.CharField(label='レビュー内容', max_length=100, required=False)
    first_name = forms.CharField(label='ユーザーの姓', max_length=20, required=False)
    created_at = forms.DateField(label='作成日', required=False, widget=forms.DateInput(attrs={'type': 'date'}))

class ReviewSortForm(forms.Form):
    sort_by = forms.ChoiceField(label='並べ替え', choices=[
        ('first_name', 'ユーザーの姓'),
        ('created_at', '作成日')
    ], required=False)