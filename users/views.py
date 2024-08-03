from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib import messages
from .models import Profile
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'users/login.html')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    profile_form = ProfileForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            # profile = profile_form.save(commit=False)
            # profile.user = user
            # profile.save()

            profile = user.profile
            profile.account_user_type = profile_form.cleaned_data.get('account_user_type')
            profile.address = profile_form.cleaned_data.get('address')
            profile.save()

            login(request, user)
            return HttpResponseRedirect('/dashboard/')
        else:
            return HttpResponse('Failed!')
        
    context = {'page':page, 'form':form, 'profile_form':profile_form}
    return render(request, 'users/signup.html', context)

def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')

def homePage(request):
    return render(request, 'users/homepage.html')

@login_required(login_url='login')
def userAccount(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    context = {'user': request.user, 'profile': profile}
    return render(request, 'users/dashboard.html', context)

@login_required(login_url='login')
def updateProject(request, pk):
    user_profile = Profile.objects.get(id=pk)
    form = ProfileForm(instance=user_profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {'form':form}
    return render(request, 'users/update-profile.html', context)
