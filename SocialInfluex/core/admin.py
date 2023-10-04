from django.contrib import admin

#import profile class from models.py
from .models import Profile, Post, LikePost, FollowsCount

# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowsCount)
