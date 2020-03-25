from django.urls import path
from . import views

urlpatterns = [
    path('',views.login, name='login'),
    path('login',views.login, name='login'),
    path('register',views.register, name='register'),
    path('ajax/validate_username/', views.validate_username, name='validate_username'),
    path('out_view',views.out_view)
#     path('register',views.register, name='register')
 ]