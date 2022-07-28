from django.urls import path

from . import views

app_name = 'auth'

urlpatterns = [
    path('signup/', views.user_create , name='user_create'),
]