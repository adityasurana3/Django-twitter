from django.shortcuts import render, redirect, HttpResponse
from .models import Profile
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,'home.html',{})


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
        return render(request,'tweet/profile.html',{'profiles':profiles})
    else:
        messages.warning(request,"You must be loggedin to continue...")
        return redirect('home')
    