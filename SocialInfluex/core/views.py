from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages 
from django.http import HttpResponse # to get the request, we need to import this
from django.contrib.auth.decorators import login_required #allow login user to access certain page
from .models import Profile
# Create your views here.


@login_required(login_url='signin') # only login user can access home page
def index(request):
    return render(request, 'index.html')

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

                # log user in and redirect to settings page

                # create a profile object for new user
                user_model = User.objects.get(username = username)
                new_profile = Profile.objects.create(user = user_model, id_user = user_model.id)
                new_profile.save()
                return redirect('signup') #change to login page after create one

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