from django.urls import path
#from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'auth'

urlpatterns = [
    path('signup/', views.user_create, name='user_create'),
    path('token/', views.token_create, name='token_create'),
    #path('token/', csrf_exempt(views.token_create), name='token_create'),
]
