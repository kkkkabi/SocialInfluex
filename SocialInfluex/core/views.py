import math

from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages 
from django.http import HttpResponse # to get the request, we need to import this
from django.contrib.auth.decorators import login_required #allow login user to access certain page
from .models import Profile, Post, LikePost, FollowsCount

# Create your views here.


@login_required(login_url='signin') # only login user can access home page
def index(request):

    # GET USER PROFILE
    user_object = User.objects.get(username = request.user.username) # 1. get the username
    user_profile = Profile.objects.get(user=user_object) #2. get the profile of the user

    # POST FEED
    posts = Post.objects.all()
    return render(request, 'index.html', {'user_profile': user_profile, 'posts':posts})

@login_required(login_url='signin')
def upload(request):
    if request.method == "POST":
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user = user, image = image, caption = caption)
        new_post.save()
        return redirect('/')
    
    else:
        return redirect('/') #if post, redirect to homepage


@login_required(login_url='signin')
def like_post(request):
    username = request.user.username #get the current username
    post_id = request.GET.get('post_id') #get the post id of the liked post
    
    post = Post.objects.get(id = post_id)

    like_filter = LikePost.objects.filter(post_id = post_id, username = username).first()
    
    #if someone likes this post, cross check if the name is in LikePost database
    if like_filter == None: 
        new_like = LikePost.objects.create(post_id = post_id, username = username)
        new_like.save()
        post.no_of_likes = post.no_of_likes +1 
        post.save()
        return redirect('/')
    
    # if someone unlike the post
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes -1 
        post.save()    
        return redirect('/')


@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user = user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)  # number of post


    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method =='POST':
        follower = request.POST['follower']
        user = request.POST['user']

    #if the profile user hasn been followed, unfollowed (deleted)
        if FollowsCount.objects.filter(follower = follower, user = user).first():  #if exists
            delete_follower = FollowsCount.objects.get(follower = follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user) #back to the user page
        else:
            new_follower = FollowsCount.objects.create(follower = follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)

    else:
        return redirect('/')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user = request.user)

    # if user is updating the profile image
    if request.method == 'POST':

        # if user doesn't add new image, remain the same
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        return redirect('settings')

    return render(request, 'setting.html', {'user_profile': user_profile})


def signup(request):
    # if the data has been post, get the value of the data using the name
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']                        
        # set password criteria
        if password == password2:

            # check if the e-mail exist in the email list
            if User.objects.filter(email = email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            
            # check if the username is taken
            elif User.objects.filter(username = username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            
            # if username is not taken, create a new user
            else: 
                user = User.objects.create_user(username = username, email= email, password=password)
                user.save()

                # user login-> create a new profile-> redirect to setting page
                # log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password = password)
                auth.login(request, user_login)

                # create a profile object for new user
                user_model = User.objects.get(username = username)
                new_profile = Profile.objects.create(user = user_model, id_user = user_model.id)
                new_profile.save()
                return redirect('settings') #change to setting page after create profile

        else: 
            messages.info(request, 'Password Not Matching')
            return redirect('signup')


    else:
        return render(request, 'signup.html')  #it will go to templates/signuphtml
    

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password = password)

        if user is not None: #if the user is registered, redirect to the homepage
            auth.login(request, user)
            return redirect('/')
        else: # if the user is not registered, report error message and redirect to signin page
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')
        
    else:
        return render(request, 'signin.html')


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')