
from django.urls import path
from . import views

urlpatterns = [
    # path('',views.dash,name='dash'),
    path('',views.dashboard, name='dashboard')
]
