from django.contrib import admin

from twit.models import Tweet
from twit.models import Followers
from twit.models import Followings

# Register your models here.
admin.site.register(Tweet)
admin.site.register(Followers)
admin.site.register(Followings)