from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from twit import models
from django.contrib.auth.models import User
from twit.models import Tweet


from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

from .forms import UserLoginForm, UserRegisterForm , AddTweetForm

@login_required
def home(request):
    if request.method == "GET":
        form = AddTweetForm()
        tweets = Tweet.objects.all().order_by('-created')
        users = User.objects.all()
        context = {'form': form,
                   'tweet': tweets,
                   'user': users}

        return render(request, "home.html", context)



    form= AddTweetForm(request.POST or None)
    if form.is_valid():
        newtweet = models.Tweet()
        newtweet.author = request.user
        newtweet.tweet = form.cleaned_data['tweet']
        newtweet.save()
    context = {'form': form}

    return render(request, "Tweeted.html", context )



@login_required
def profile(request, pk = None):
    if pk:
        user = User.objects.get(pk=pk)
        context = {'user': user}
        return render(request, 'profile.html', context)
    else:
        user = request.user
    tweet = Tweet.objects.filter(author=user)
    context = {'user': user, 'tweet': tweet}
    return render(request, 'profile.html', context)

def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form,
    }
    return render(request, "login.html", context)


def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form,
    }
    return render(request, "signup.html", context)


def logout_view(request):
    logout(request)
    return redirect('/')