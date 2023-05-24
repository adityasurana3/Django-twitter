from django.shortcuts import render, redirect, HttpResponse
from .models import Profile, Tweet
from django.contrib import messages
from .forms import TweetForm, SignUpForm
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        form = TweetForm()
        if request.method == 'POST':
            form = TweetForm(request.POST)
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                messages.success(request, 'Your tweet has been Posted')
                return redirect('home')
        tweets = Tweet.objects.all().order_by('-created_at')
        return render(request, 'home.html', {'tweets': tweets, 'form': form})
    else:
        tweets = Tweet.objects.all().order_by('-created_at')
        return render(request, 'home.html', {'tweets': tweets})


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'tweet/profile_list.html', {'profiles': profiles})
    else:
        messages.warning(request, "You must be loggedin to continue...")
        return redirect('home')


def profile(request, pk):
    if request.user.is_authenticated:
        profiles = Profile.objects.get(user__id=pk)
        tweets = Tweet.objects.filter(user__id=pk)
        if request.method == "POST":

            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == "unfollow":
                current_user_profile.follows.remove(profiles)
            elif action == "follow":
                current_user_profile.follows.add(profiles)
            else:
                print("something went wrong")
            current_user_profile.save()
        return render(request, 'tweet/profile.html', {'profiles': profiles, 'tweets': tweets})
    else:
        messages.warning(request, "You must be loggedin to continue...")
        return redirect('login')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.warning(request, "You have been loggedin")
            return redirect('home')
        else:
            messages.warning(request, "There was an error loggin in")
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.warning(request, "You are logged out")
    return redirect('login')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                messages.success(request, 'Your account was created successfully')
                return redirect('home')
            print(password,username)
    else:
        form = SignUpForm()
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)
