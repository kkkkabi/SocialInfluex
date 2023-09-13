# not default file, need to create

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'), #''means home page
    path('signup',views.signup, name = 'signup'),
    path('signin',views.signin, name= 'signin'),
    path('logout',views.logout, name= 'logout'),

]