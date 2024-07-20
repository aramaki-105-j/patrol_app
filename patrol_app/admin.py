from django.contrib import admin
from .models import CustomUser, Marker, Review, TopImage, SelfIntroduction

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'address')
    search_fields = ('first_name', 'last_name', 'address')

@admin.register(Marker)
class MarkerAdmin(admin.ModelAdmin):
    list_display = ('id', 'lat', 'lng')
    search_fields = ('lat', 'lng')

@admin.register(SelfIntroduction)
class SelfIntroductionAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'second_image')  
    search_fields = ('id',) 

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Review)
admin.site.register(TopImage)
