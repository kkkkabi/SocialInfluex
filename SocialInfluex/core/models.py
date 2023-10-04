from django.db import models
from django.contrib.auth import get_user_model
import uuid #generate unique id for post
from datetime import datetime #get datetime of 

# Everytime we use this user, it will be currently logging in user
User = get_user_model()


# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE) #foreign key that is linking to that model
    id_user = models.IntegerField() #ID of the user to access the profile, interger
    bio = models.TextField(blank = True) # user migh
    profileimg = models.ImageField(upload_to='profile_images', default= 'blank_profile.png') #profile Image
    location = models.CharField(max_length=100, blank=True) 

#this is not compulsory, just name of the model and we can see it in admin pannel.
    def __str__(self):
        return self.user.username
    

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)  #username
    image = models.ImageField(upload_to='post_image')
    caption = models.TextField(blank=True)
    created_at = models.DateField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
class FollowsCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user