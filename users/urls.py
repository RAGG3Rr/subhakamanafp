from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from allauth.account.views import PasswordSetView

urlpatterns = [
    path('register/', views.registerIndividual, name='register'),
    path('organization-register/',views.registerorganization,name="organisationregister"),
    path('profile/', views.profile, name='profile'),
    path('delete_profile/<int:pk>', views.DeleteProfile, name='delete_user'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('set_password/', views.MyPasswordSetView.as_view(template_name='users/set_password.html'), name='account_set_password'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='users/changepassword.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='users/passwordchanged.html'), name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='reset_password'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'), 
	
	
	path('adduser/', views.adduser, name='adduser'),
]

