from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from allauth.account import views
from django.views import View
from patrol_app.models import CustomUser
from patrol_app.forms import ProfileForm

class TopView(TemplateView):
   template_name = 'Top.html'

class ProfileView(View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)

        return render(request, 'account/profile.html', {
            'user_data': user_data,
        })

class ProfileEditView(View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)
        form = ProfileForm(
            request.POST or None,
            initial={
                'first_name': user_data.first_name,
                'last_name': user_data.last_name,
                'email': user_data.email,
                'telephone_number': user_data.telephone_number,
                'post_code': user_data.post_code,
                'address': user_data.address,
            }
        )

        return render(request, 'account/profile_edit.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST or None)
        if form.is_valid():
            user_data = CustomUser.objects.get(id=request.user.id)
            user_data.first_name = form.cleaned_data['first_name']
            user_data.last_name = form.cleaned_data['last_name']
            user_data.email = form.cleaned_data['email']
            user_data.telephone_number = form.cleaned_data['telephone_number']
            user_data.post_code = form.cleaned_data['post_code']
            user_data.address = form.cleaned_data['address']
            
            user_data.save()
            return redirect('profile')

        return render(request, 'registration/profile.html', {
            'form': form
        })


