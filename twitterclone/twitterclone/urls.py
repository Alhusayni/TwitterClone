"""twitterclone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from twit.views import home
from django.conf import settings
from django.conf.urls.static import static
from twit.views import login_view, register_view, logout_view, profile, follow, unfollow,timeline,details,liketweets,likepage,deletetweet

# Routes
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/register/', register_view, name='signup'),
    path('accounts/logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/<int:pk>/', profile, name='profile_pk'),
    path('follow/<int:pk>/', follow, name='follow'),
    path('unfollow/<int:pk>/', unfollow, name='unfollow'),
    path('timeline/', timeline , name ='timeline'),
    path('tweet/<int:id>/', details, name='details'),
    path('like/', liketweets, name='liketweet'),
    path('liketweet/', likepage, name = 'likepage'),
    path('removetweet/', deletetweet, name= 'deletetweet')

]

# Handling the saving media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
