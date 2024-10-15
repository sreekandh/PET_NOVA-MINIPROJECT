from django.urls import path
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import (
    register_trainer, activate_trainer, deactivate_trainer, view_trainers,
    send_trainer_email
)
from .views import register_caretaker, view_caretakers, activate_caretaker, deactivate_caretaker, send_caretaker_email


urlpatterns = [
    # Admin and Authentication Paths
    path('admin_function/', views.admin_function, name='admin_function'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('trainer_home/', views.trainer_home, name='trainer_home'),
    path('caretaker_home/', views.caretaker_home, name='caretaker_home'),
    path('logout/', views.user_logout, name='logout'),

    # User and Admin User Management Paths
    path('admin/users/', views.admin_users, name='admin_users'),
    path('view_registered_users/', views.view_registered_users, name='view_registered_users'),

    # Pet Management Paths (Cats)
    path('cats/', views.view_cats, name='view_cats'),
    path('add_cat/', views.add_cat, name='add_cat'),
    path('edit_cat/<int:cat_id>/', views.edit_cat, name='edit_cat'),
    path('delete_cat/<int:cat_id>/', views.delete_cat, name='delete_cat'),

    # Pet Management Paths (Dogs)
    path('dogs/', views.view_dogs, name='view_dogs'),
    path('add_dog/', views.add_dog, name='add_dog'),
    path('edit_dog/<int:dog_id>/', views.edit_dog, name='edit_dog'),
    path('delete_dog/<int:dog_id>/', views.delete_dog, name='delete_dog'),

    # Adoption Process Paths
    path('apply/<int:pet_id>/<str:pet_type>/', views.apply_for_adoption, name='apply_for_adoption'),
    path('approve/<int:application_id>/', views.approve_application, name='approve_application'),
    path('disapprove/<int:application_id>/', views.disapprove_application, name='disapprove_application'),
    path('applications/', views.view_applications, name='view_applications'),
    path('adoption_success/', views.adoption_success, name='adoption_success'),
    path('make_payment/<int:application_id>/', views.make_payment, name='make_payment'),
    path('payment_success/', views.payment_success, name='payment_success'),
    
    # Staff Management Paths (Trainers)
    path('register_trainer/', register_trainer, name='register_trainer'),
    path('view_trainers/', view_trainers, name='view_trainers'),  # View trainers
    path('deactivate_trainer/<int:id>/', deactivate_trainer, name='deactivate_trainer'),  # Deactivate trainer
    path('activate_trainer/<int:id>/', activate_trainer, name='activate_trainer'),  # Activate trainer
    path('send_email/<int:trainer_id>/', send_trainer_email, name='send_trainer_email'),  # Send email to trainer

    # Staff Management Paths (Caretakers)
   path('register_caretaker/', register_caretaker, name='register_caretaker'),
    path('view_caretakers/', view_caretakers, name='view_caretakers'),
    path('caretakers/activate/<int:id>/', activate_caretaker, name='activate_caretaker'),
    path('caretakers/deactivate/<int:id>/', deactivate_caretaker, name='deactivate_caretaker'),
    path('caretakers/send_email/<int:caretaker_id>/', send_caretaker_email, name='send_caretaker_email'),

    # Miscellaneous and Extra Functionality Paths
    path('apply_control/', views.apply_control, name='apply_control'),
    path('view_pets/', views.view_pets, name='view_pets'),
    path('add_pets/', views.add_pets, name='add_pets'),
    path('staff_control/', views.staff_control, name='staff_control'),
    path('trainer_con/', views.trainer_con, name='trainer_con'),
    path('caretaker_con/', views.caretaker_con, name='caretaker_con'),
    
    # Pet Information Paths (separate routes for cat and dog views)
    path('cat/', views.cat, name='cat'),
    path('dog/', views.dog, name='dog'),


        path('trainer/profile/', views.trainer_profile, name='trainer_profile'),
    path('trainers/view_slots/<int:trainer_id>/', views.view_training_slots, name='view_training_slots'),

path('book_slot/<int:slot_id>/', views.book_training_slot, name='book_training_slot'),

    path('user_view_trainers/', views.user_view_trainers, name='user_view_trainers'),


 
      path('slots/', views.list_training_slots, name='list_training_slots'),
    path('slots/add/', views.add_training_slot, name='add_training_slot'),
    path('slots/edit/<int:slot_id>/',views.edit_training_slot, name='edit_training_slot'),
    path('slots/delete/<int:slot_id>/', views.delete_training_slot, name='delete_training_slot'),



      path('user/training-slots/', views.user_list_training_slots, name='user_list_training_slots'),
    # Add other URL patterns here
    path('trainer/slot/booking/<int:slot_id>/', views.trainer_slot_booking_view, name='trainer_slot_booking_view'),


    path('admin/bookings/', views.admin_view_bookings, name='admin_view_bookings'),


    path('book_slot/', views.book_caretaker_slot, name='book_slot'),


 path('assign-caretaker-slot/', views.assign_caretaker_slot, name='assign_caretaker_slot'),

    # URL for viewing caretaker slots (Users view available slots)
path('caretaker-slots/', views.list_caretaker_slots, name='list_caretaker_slots'),
    path('caretaker-slots/edit/<int:slot_id>/', views.edit_caretaker_slot, name='edit_caretaker_slot'),
    path('caretaker-slots/delete/<int:slot_id>/', views.delete_caretaker_slot, name='delete_caretaker_slot'),


    path('user_view_caretaker/', views.user_view_caretaker, name='user_view_caretaker'),  # URL to view all caretakers
    path('caretaker/<int:caretaker_id>/book/', views.book_caretaker_slot, name='book_caretaker_slot'),

path('booking-success/', views.booking_success, name='booking_success'),



    path('admin/caretaker-bookings/', views.admin_user_caretaker_view, name='admin_user_caretaker_view'),




    path('my-caretaker-bookings/', views.user_caretaker_bookings, name='user_caretaker_bookings'),



    path('payment/<int:booking_id>/', views.payment_page, name='payment_page'),


 path('payment/success/', views.payment_success, name='payment_success'),

    # Booking cancellation URL
    path('booking/cancel/<int:booking_id>/', views.booking_cancel, name='booking_cancel'),


    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),



    path('book_trainer_slot/<int:trainer_id>/', views.book_trainer_slot, name='book_trainer_slot'),


    path('trainer/payment/<int:booking_id>/', views.trainer_payment_page, name='trainer_payment_page'),

     path('my-trainer-bookings/', views.user_trainer_bookings, name='user_trainer_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('trainer-bookings/', views.admin_user_trainer_view, name='admin_user_trainer_view'),  # Add this line

]

# Static and Media Files Configuration
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


'''

  path('caretaker/schedule/', views.assign_caretaker_slots, name='caretaker_schedule'),

  

from .views import add_trainer, view_trainers, edit_trainer, delete_trainer

    path('schedule_training_section/', views.schedule_training_section, name='schedule_training_section'),




 path('trainers/add/', add_trainer, name='add_trainer'),
    path('trainers/', view_trainers, name='view_trainers'),
    path('trainers/edit/<int:trainer_id>/', edit_trainer, name='edit_trainer'),
    path('trainers/delete/<int:trainer_id>/', delete_trainer, name='delete_trainer'),


    from .views import add_caretaker, view_caretakers, edit_caretaker, delete_caretaker

    path('caretakers/add/', add_caretaker, name='add_caretaker'),
    path('caretakers/', view_caretakers, name='view_caretakers'),
    path('caretakers/edit/<int:caretaker_id>/', edit_caretaker, name='edit_caretaker'),
    path('caretakers/delete/<int:caretaker_id>/', delete_caretaker, name='delete_caretaker'),

    


     path('manage_slots/', views.manage_training_slots, name='manage_training_slots'),
    path('delete_slot/<int:slot_id>/', views.delete_training_slot, name='delete_training_slot'),
    path('update_slot/<int:slot_id>/', views.update_training_slot, name='update_training_slot'),
'''