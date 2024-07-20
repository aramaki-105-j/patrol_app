from django.urls import path, include
from patrol_app import views, credit
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.self_introduction_view, name='self_introduction'),

    path('top/', views.TopImageView.as_view(), name='top'),
    path('top_image_create/', views.TopImageCreateView.as_view(), name='top_image_create'),
    path('topimage_delete/<int:pk>/', views.TopImageDeleteView.as_view(), name='topimage_delete'),


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
    path('review/<int:pk>/delete/',  views.ReviewDeleteView.as_view(), name='review_delete'),
    path('review/<int:pk>/edit/', views.ReviewUpdateView.as_view(), name='review_edit'),

    path('credit/register/', credit.CreditRegisterView.as_view(), name='credit_register'),
    path('credit/update/', credit.CreditUpdateView.as_view(), name='credit_update'),
    path('subscription/cancel/', credit.SubscriptionCancelView.as_view(), name='subscription_cancel'),
    path('subscription_complete/', credit.SubscriptionCompleteView.as_view(), name='subscription_complete'),
    path('subscription/cancel/complete/', credit.SubscriptionCancelCompleteView.as_view(), name='subscription_cancel_complete'),
    path('credit/update/complete/', credit.CreditUpdateCompleteView.as_view(), name='credit_update_complete'),

]