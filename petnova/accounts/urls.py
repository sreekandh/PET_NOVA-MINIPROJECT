from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView  # Add this import
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    
    # Password reset views
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('user_profile/', views.user_profile, name='user_profile'),
    path('user_profile/edit/', views.edit_profile, name='edit_profile'),

    path('admin_home/', views.admin_home, name='admin_home'),
    path('trainer_home/', views.trainer_home, name='trainer_home'),
    path('caretaker_home/', views.caretaker_home, name='caretaker_home'),
    
    # Logout URL with redirection to the login page
    path('logout/', LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
]
