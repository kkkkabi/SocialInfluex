# not default file, need to create

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'), #''means home page
    path('settings',views.settings, name = 'settings'),
    path('upload', views.upload, name = 'upload'),
    path('follow', views.follow, name = 'follow'),
    path('profile/<str:pk>', views.profile, name = 'profile'),
    path('like-post', views.like_post, name = 'like-post'),
    path('signup',views.signup, name = 'signup'),
    path('signin',views.signin, name= 'signin'),
    path('logout',views.logout, name= 'logout'),

]