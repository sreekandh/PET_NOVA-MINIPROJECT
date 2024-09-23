from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import cat_list, dog_list, cat_detail, dog_detail


urlpatterns = [
    path('',views.home,name='home'),
        path('pet_details/',views.pet_details,name='pet_details'),
            path('pet_details/<str:pet_name>/', views.pet_details, name='pet_details'),

    

      path('pets/', views.pet_list, name='pet_list'),
    path('pets/create/', views.pet_create, name='pet_create'),
    path('pets/<int:pk>/edit/', views.pet_update, name='pet_update'),
    path('pets/<int:pk>/delete/', views.pet_delete, name='pet_delete'),
    path('pets/cats/', lambda r: views.pet_list(r, category='Cat'), name='cat_details'),
    path('pets/dogs/', lambda r: views.pet_list(r, category='Dog'), name='dog_details'),
       path('pets/<str:category>/', views.pet_list, name='pet_list_by_category'),
    path('pets/<int:pk>/', views.pet_detail, name='pet_detail'),

    path('cats/', cat_list, name='cat_list'),
    path('dogs/', dog_list, name='dog_list'),
    path('cats/<int:cat_id>/', cat_detail, name='cat_detail'),
    path('dogs/<int:dog_id>/', dog_detail, name='dog_detail'),

     path('app_view/',views.app_view,name='app_view'),
         

]


"""   path('make_payment/<int:application_id>/', views.make_payment, name='make_payment'),
    path('payment_success/<int:application_id>/', views.payment_success, name='payment_success'),
  path('cat_details/',views.cat_details,name='cat_details'),
    path('dog_details/',views.dog_details,name='dog_details'),"""