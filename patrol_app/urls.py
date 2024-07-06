from django.urls import path, include
from patrol_app import views

urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('account/', include('allauth.urls')),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('map/', views.MapView.as_view(), name='map'),
]