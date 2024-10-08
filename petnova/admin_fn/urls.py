from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import add_trainer, view_trainers, edit_trainer, delete_trainer


urlpatterns = [
    path('admin_function/',views.admin_function,name='admin_function'),
  path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('trainer_home/', views.trainer_home, name='trainer_home'),
    path('caretaker_home/', views.caretaker_home, name='caretaker_home'),
    path('logout/', views.user_logout, name='logout'),
 path('admin/users/', views.admin_users, name='admin_users'),
 
  path('cats/', views.view_cats, name='view_cats'),
    path('dogs/', views.view_dogs, name='view_dogs'),
    path('add_cat/', views.add_cat, name='add_cat'),
    path('edit_cat/<int:cat_id>/', views.edit_cat, name='edit_cat'),
    path('delete_cat/<int:cat_id>/', views.delete_cat, name='delete_cat'),
    path('add_dog/', views.add_dog, name='add_dog'),
    path('edit_dog/<int:dog_id>/', views.edit_dog, name='edit_dog'),
    path('delete_dog/<int:dog_id>/', views.delete_dog, name='delete_dog'),
    path('view_registered_users/', views.view_registered_users, name='view_registered_users'),


  path('apply/<int:pet_id>/<str:pet_type>/', views.apply_for_adoption, name='apply_for_adoption'),
    path('approve/<int:application_id>/', views.approve_application, name='approve_application'),
    path('disapprove/<int:application_id>/', views.disapprove_application, name='disapprove_application'),

    path('adoption_success/', views.adoption_success, name='adoption_success'),

        path('applications/', views.view_applications, name='view_applications'),

    path('make_payment/<int:application_id>/', views.make_payment, name='make_payment'),
        path('payment_success/', views.payment_success, name='payment_success'),  # Add this line

        path('apply_control/',views.apply_control,name='apply_control'),
         path('view_pets/',views.view_pets,name='view_pets'),
                  path('add_pets/',views.add_pets,name='add_pets'),
                               path('staff_control/',views.staff_control,name='staff_control'),
                               path('trainer_con/',views.trainer_con,name='trainer_con'),
                               path('caretaker_con/',views.caretaker_con,name='caretaker_con'),



   path('trainers/add/', add_trainer, name='add_trainer'),
    path('trainers/', view_trainers, name='view_trainers'),
    path('trainers/edit/<int:trainer_id>/', edit_trainer, name='edit_trainer'),
    path('trainers/delete/<int:trainer_id>/', delete_trainer, name='delete_trainer'),
 path('cat/', views.cat, name='cat'),
path('dog/', views.dog, name='dog'),


]