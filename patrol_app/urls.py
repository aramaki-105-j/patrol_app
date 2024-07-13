from django.urls import path, include
from patrol_app import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('account/', include('allauth.urls')),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),

    path('map/', views.MapView.as_view(), name='map'),
    path('get_markers/', views.MarkerListView.as_view(), name='get_markers'),
    path('add_marker/', views.MarkerCreateView.as_view(), name='add_marker'),
    path('update_marker/', views.MarkerUpdateView.as_view(), name='update_marker'),
    path('delete_marker/', views.MarkerDeleteView.as_view(), name='delete_marker'),
    path('marker_detail/<int:pk>/', views.MarkerDetailView.as_view(), name='marker_detail'),
    
    path('marker/<int:marker_id>/review_create/', views.ReviewCreateView.as_view(), name='review_create'),
] 