from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    path('admin_function/',views.admin_function,name='admin_function'),
  path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('trainer_home/', views.trainer_home, name='trainer_home'),
    path('caretaker_home/', views.caretaker_home, name='caretaker_home'),
    path('logout/', views.user_logout, name='logout'),

]