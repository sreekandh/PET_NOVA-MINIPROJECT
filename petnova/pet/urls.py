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
    

      path('pets/', views.pet_list, name='pet_list'),
    path('pets/create/', views.pet_create, name='pet_create'),
    path('pets/<int:pk>/edit/', views.pet_update, name='pet_update'),
    path('pets/<int:pk>/delete/', views.pet_delete, name='pet_delete'),
    path('pets/cats/', lambda r: views.pet_list(r, category='Cat'), name='cat_details'),
    path('pets/dogs/', lambda r: views.pet_list(r, category='Dog'), name='dog_details'),
       path('pets/<str:category>/', views.pet_list, name='pet_list_by_category'),
    path('pets/<int:pk>/', views.pet_detail, name='pet_detail'),
]


