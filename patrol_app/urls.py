from django.urls import path, include
from patrol_app import views

urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('account/', include('allauth.urls')),
]