from django.shortcuts import render, redirect, HttpResponse
from .models import Profile, Tweet
from django.contrib import messages

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        tweets = Tweet.objects.all().order_by('-created_at')
    return render(request,'home.html',{'tweets':tweets})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request,'tweet/profile_list.html',{'profiles':profiles})
    else:
        messages.warning(request,"You must be loggedin to continue...")
        return redirect('home')
    
def profile(request,pk):
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
        return render(request,'tweet/profile.html',{'profiles':profiles,'tweets':tweets})
    else:
        messages.warning(request,"You must be loggedin to continue...")
        return redirect('home')
    