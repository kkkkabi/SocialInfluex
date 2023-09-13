from django.db import models
from django.contrib.auth import get_user_model


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