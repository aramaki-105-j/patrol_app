from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from allauth.account import views
from django.views import View
from patrol_app.models import CustomUser, Marker
from patrol_app.forms import ProfileForm
from django.conf import settings
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class TopView(TemplateView):
   template_name = 'top.html'

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

class MapView(TemplateView):
    template_name = 'map.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['GOOGLE_MAPS_API_KEY'] = settings.GOOGLE_MAPS_API_KEY
        return context

class MarkerListView(View):
    def get(self, request):
        markers = Marker.objects.all()
        marker_list = [{'id': marker.id, 'lat': marker.lat, 'lng': marker.lng} for marker in markers]
        return JsonResponse(marker_list, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class MarkerCreateView(View):
    def post(self, request):
        data = json.loads(request.body)
        lat = data.get('lat')
        lng = data.get('lng')
        if lat and lng:
            Marker.objects.create(lat=lat, lng=lng)
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Invalid data'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class MarkerUpdateView(View):
    def post(self, request):
        data = json.loads(request.body)
        marker_id = data.get('id')
        lat = data.get('lat')
        lng = data.get('lng')
        if marker_id and lat and lng:
            marker = get_object_or_404(Marker, id=marker_id)
            marker.lat = lat
            marker.lng = lng
            marker.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Invalid data'}, status=400)