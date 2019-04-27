from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from twit import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from twit.models import Tweet, Followings


from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

from .forms import UserLoginForm, UserRegisterForm , AddTweetForm


# To render the home page, If it's GET request show the main home page,
# If it's POST "user tweet" show them Tweeted post and redirect them to Home Page again
# @login_required to not allowing unregistered user to visit this page
@login_required
def home(request):
    if request.method == "GET":
        form = AddTweetForm()
        tweets = Tweet.objects.all().order_by('-created')
        users = User.objects.exclude(username = request.user)
        follos = Followings.objects.get(userid=request.user)
        followings = follos.following.all()
        context = {'form': form,
                   'tweet': tweets,
                   'user': users,
                   'following': followings}

        return render(request, "home.html", context)
    form = AddTweetForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        newtweet = models.Tweet()
        newtweet.author = request.user
        newtweet.tweet = form.cleaned_data['tweet']
        try:
            newtweet.image = request.FILES['upload_media']
        except:
            newtweet.image = None
        newtweet.save()
    context = {'form': form}

    return render(request, "Tweeted.html", context )


# To render the profile page,
# if the profile is the owner of the account show them "His tweet, and His following, and able to delete his tweets"
# if the profile for any other user, show him only his information
# @login_required to not allowing unregistered user to visit this page
@login_required
def profile(request, pk = None):
    if pk:
        user = User.objects.get(pk=pk)
        context = {'user': user}
        return render(request, 'profile.html', context)
    else:
        user = request.user
    tweet = Tweet.objects.filter(author=user).order_by('-created')
    follos = Followings.objects.get(userid=user)
    followings = follos.following.all()
    context = {'user': user,
               'tweet': tweet,
               'following': followings,
               'follow': follos}
    return render(request, 'profile.html', context)

# To render the login Page
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

# To render the register page
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


# To logout from the website
def logout_view(request):
    logout(request)
    return redirect('/')


# To allow the user to follow other users in the website
# @login_required to not allowing unregistered user to do this
@login_required
def follow(request, pk):
    nuser = User.objects.get(pk=pk)
    Followings.make_follow(request.user, nuser)
    return redirect('/')

# To allow the user to unfollow users that he is already followed them
# @login_required to not allowing unregistered user to do this
@login_required
def unfollow(request, pk):
    nuser = User.objects.get(pk=pk)
    Followings.unfollow(request.user, nuser)
    return redirect('/')


# To render a page that show the tweets of people that the user followed them only
# @login_required to not allowing unregistered user to do this
@login_required
def timeline(request):
    follos = Followings.objects.get(userid=request.user)
    followings = follos.following.all()
    tweet = Tweet.objects.filter(author__in= followings).order_by('-created')

    context = {'tweets': tweet}

    return render(request, 'timeline.html', context)


# To render a page that show the details of tweets
# @login_required to not allowing unregistered user to visit this page
@login_required
def details(request, id):
    tweet = Tweet.objects.filter(id = id)
    twet = Tweet.objects.get(id = id)
    is_liked = False
    if twet.like.filter(id=request.user.id).exists():
        is_liked = True

    context = {'tweet' : tweet,
               'is_liked': is_liked,
               'total': twet.total()}
    return render (request, 'details.html', context)


# To let the user to like or unlike the tweet in the details page
# @login_required to not allowing unregistered user to do this
@login_required
def liketweets(request):
    twet = get_object_or_404(Tweet, id=request.POST.get('tweetid'))
    is_liked = False
    if twet.like.filter(id=request.user.id).exists():
        twet.like.remove(request.user)
        is_liked = False
    else:
        twet.like.add(request.user)
        is_liked = True
    url = ('/tweet/'+str(twet.id))
    return redirect(url)


# To render a page that shows only the tweets that the user liked it only
# @login_required to not allowing unregistered user to visit this page
@login_required
def likepage(request):
    twet = Tweet.objects.filter(like=request.user).order_by('-created')

    context = {'tweet': twet}

    return render(request, 'likedtweet.html', context)


# To let the user delete his tweets in his profile page and only the owner user able to delete his tweet
# @login_required to not allowing unregistered user to do this
@login_required
def deletetweet(request):
    get_object_or_404(Tweet, id=request.POST.get('tweetid')).delete()
    return redirect('/')
