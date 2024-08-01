from django.shortcuts import render
import mysql.connector as sql
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.cache import cache_control
#from django.contrib.auth.decorators import login_required


# Create your views here.

uname=''
emailid=''
pwd=''
cpwd=''
flag='Y'

#@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def HomePage(request):
    return render (request,'home.html')

def LoginPage(request):
    logout(request)
   
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # If user is valid, log them in
            auth_login(request, user)
            return redirect('home')  # Replace 'home' with your desired URL
        else:
            messages.error(request, 'Invalid username or password.')

    
    return render (request,'login.html')

def SignupPage(request):
    
    global uname,emailid,pwd
    
    if request.method=='POST':
        m=sql.connect(host='localhost',username='root',passwd='root', db='django')
        cursor=m.cursor()
        d=request.POST
        
        for key,val in d.items():
            if key=='username':
                uname=val
            elif key=='email':
                emailid=val
            elif key=='password':
                pwd=val
            elif key=='confirm_password':
                cpwd=val
        
        if pwd == cpwd:
            if User.objects.filter(username=uname).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=emailid).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(username=uname, email=emailid, password=pwd)
                user.save()
                
                query=f"INSERT INTO USER VALUES ('{uname}','{emailid}','{pwd}')"
                cursor.execute(query)
                m.commit()
                messages.success(request, 'Account created successfully')
                return redirect('login')  # Redirect to login page after successful signup
                
        else:
            messages.error(request, 'Passwords do not match')  
    
    return render (request,'signup.html')


def latest(request):
    return render(request, 'latest.html')

def about(request):
    return render(request, 'about.html')

def logoutpage(request):
    logout(request)
    messages.info(request, 'Logged Out Successfully!')
    return render(request, 'logout.html')

