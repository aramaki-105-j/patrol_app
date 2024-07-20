from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.shortcuts import render, redirect
from allauth.account import views
from django.views import View
from patrol_app.models import CustomUser, Marker, Review, TopImage, SelfIntroduction
from patrol_app.forms import ProfileForm, ReviewForm, ReviewSearchForm, ReviewSortForm, TopImageCreateForm
from django.conf import settings
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import reverse_lazy

def self_introduction_view(request):
    self_intro = SelfIntroduction.objects.first()
    return render(request, 'self_introduction.html', {'self_intro': self_intro})

def top_view(request):
    images = TopImage.objects.all()
    return render(request, 'top.html', {'images': images})

class TopImageCreateView(UserPassesTestMixin, CreateView):
    template_name = 'topimegecreate_form.html'
    model = TopImage
    form_class = TopImageCreateForm

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_paid

    def handle_no_permission(self):
        return redirect('top')
    
    def post(self, request, *args, **kwargs):
        form = TopImageCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('top')
        return render(request, 'topimegecreate_form.html', {'form': form})

class TopImageDeleteView(UserPassesTestMixin, DeleteView):
    model = TopImage
    template_name = 'topimage_delete_confirm.html'
    success_url = reverse_lazy('top')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_paid

    def handle_no_permission(self):
        return redirect('top')

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

@method_decorator(csrf_protect, name='dispatch')
class MarkerCreateView(View):
    def post(self, request):
        data = json.loads(request.body)
        lat = data.get('lat')
        lng = data.get('lng')
        if lat and lng:
            Marker.objects.create(lat=lat, lng=lng)
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Invalid data'}, status=400)

@method_decorator(csrf_protect, name='dispatch')
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

@method_decorator(csrf_protect, name='dispatch')
class MarkerDeleteView(View):
    def post(self, request):
        data = json.loads(request.body)
        marker_id = data.get('id')
        if marker_id:
            marker = get_object_or_404(Marker, id=marker_id)
            marker.delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Invalid data'}, status=400)

class MarkerDetailView(LoginRequiredMixin, DetailView):
    model = Marker
    template_name = 'marker_detail.html'
    context_object_name = 'marker'
    login_url = '/login/' 
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        marker = self.get_object()
        reviews = Review.objects.filter(marker=marker)

        # 検索フォームの処理
        search_form = ReviewSearchForm(self.request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data.get('query')
            first_name = search_form.cleaned_data.get('first_name')
            created_at = search_form.cleaned_data.get('created_at')

            if query:
                reviews = reviews.filter(content__icontains=query)
            if first_name:
                reviews = reviews.filter(user__first_name__icontains=first_name)
            if created_at:
                reviews = reviews.filter(created_at__date=created_at)

        # 並べ替えフォームの処理
        sort_form = ReviewSortForm(self.request.GET)
        if sort_form.is_valid():
            sort_by = sort_form.cleaned_data.get('sort_by')
            if sort_by:
                if sort_by == 'first_name':
                    reviews = reviews.order_by('user__first_name')
                elif sort_by == 'created_at':
                    reviews = reviews.order_by('-created_at')

        # ページネーションの処理
        paginator = Paginator(reviews, 10) 
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['reviews'] = page_obj
        context['search_form'] = search_form
        context['sort_form'] = sort_form
        return context

class ReviewCreateView(LoginRequiredMixin, View):
    form_class = ReviewForm
    template_name = 'review_create.html'

    def get(self, request, marker_id):
        marker = get_object_or_404(Marker, id=marker_id)
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'marker': marker})

    def post(self, request, marker_id):
        marker = get_object_or_404(Marker, id=marker_id)
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.marker = marker
            review.user = request.user
            review.save()
            return redirect('marker_detail', pk=marker.id)
        return render(request, self.template_name, {'form': form, 'marker': marker})

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'review_confirm_delete.html'
    context_object_name = 'review'

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user

    def get_success_url(self):
        return reverse_lazy('marker_detail', kwargs={'pk': self.object.marker.id})

class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review_update.html'
    context_object_name = 'review'

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user

    def get_success_url(self):
        return reverse_lazy('marker_detail', kwargs={'pk': self.object.marker.id})