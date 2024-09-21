from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    path('',views.home,name='home'),
        path('pet_details/',views.pet_details,name='pet_details'),
            path('pet_details/<str:pet_name>/', views.pet_details, name='pet_details'),
    path('cat_details/',views.cat_details,name='cat_details'),
    path('dog_details/',views.dog_details,name='dog_details'),
    
]


