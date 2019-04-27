from django.contrib import admin

from twit.models import Tweet
from twit.models import Followings

# Register the models to the admin page.
admin.site.register(Tweet)
admin.site.register(Followings)