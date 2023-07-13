from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import Profile, Tweet
from django.contrib import messages
from .forms import TweetForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


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
        messages.warning(request, "You must be logged in to continue...")
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
                return HttpResponse("<h1>Something went wrong...</h1>")
            current_user_profile.save()
        return render(request, 'tweet/profile.html', {'profiles': profiles, 'tweets': tweets})
    else:
        messages.warning(request, "You must be logged in to continue...")
        return redirect('login')

def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id = pk)
            return render(request, 'tweet/followers.html',{'profiles':profiles})
        else:
            messages.warning(request, "You can't access other user followers")
            return redirect('home')
    else:
        messages.warning(request, "You must be logged in to continue...")
        return redirect('login')

def follows(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id = pk)
            return render(request, 'tweet/follows.html',{'profiles':profiles})
        else:
            messages.warning(request, "You can't access other user followers")
            return redirect('home')
    else:
        messages.warning(request, "You must be logged in to continue...")
        return redirect('login')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.warning(request, "You have been logged in")
            return redirect('home')
        else:
            messages.warning(request, "There was an error. Please try again!!!")
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.warning(request, "You are logged out")
    return redirect('login')


def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Your account was created successfully')
                    return redirect('home')
        else:
            form = SignUpForm()
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)


def update_user(request, pk):
    if request.user.is_authenticated:
        current_user = User.objects.get(pk=pk)
        profile_user = Profile.objects.get(user__id = request.user.id)
        if request.method == 'POST':
            user_form = SignUpForm(request.POST, request.FILES or None, instance=current_user)
            profile_form = ProfilePicForm(request.POST, request.FILES or None, instance=profile_user)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                login(request, current_user)
                messages.success(request, 'You profile has been updated')
                return redirect('home')
        else:
            user_form = SignUpForm(instance=current_user)
            profile_form = ProfilePicForm(instance=profile_user)
        return render(request, 'tweet/update_user.html', {'user_form': user_form, 'profile_form':profile_form})
    else:
        messages.warning(request, 'You must be logged in')
        return redirect('home')

def tweet_like(request,pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet,id=pk)
        if tweet.likes.filter(id=request.user.id):
            tweet.likes.remove(request.user)
        else:
            tweet.likes.add(request.user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.warning(request, 'You must be logged in')
        return redirect('home')
    
def tweet_show(request, pk):
    tweet = get_object_or_404(Tweet,id=pk)
    if tweet:
        return render(request, 'tweet/show_tweet.html', {'tweet':tweet})
    else:
        messages.success(request, 'That tweet does not exist')
        return redirect('home')
    
def unfollow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user__id = pk)
        request.user.profile.follows.remove(profile)
        profile.save()
        messages.success(request, f'You have successfully unfollowed {profile.user.username}')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.warning(request, 'You must be logged in')
        return redirect('home')

def follow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user__id = pk)
        request.user.profile.follows.add(profile)
        profile.save()
        messages.success(request, f'You have successfully followed {profile.user.username}')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.warning(request, 'You must be logged in')
        return redirect('home')