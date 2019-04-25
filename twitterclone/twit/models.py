from django.db import models
from django.contrib.auth.models import User

class Tweet(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.CharField(max_length=280)
    created = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)
    def __str__(self):
        return self.tweet


class Followers(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE,related_name='userid')
    follower = models.ManyToManyField(User, related_name='followers' , symmetrical=False)



class Followings(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='following', symmetrical=False)
    @classmethod
    def make_follow(cls, userid, the_follower):
        follower, created= cls.objects.get_or_create(
            userid=userid

        )
        follower.userid.add(the_follower)

    @classmethod
    def unfollow(cls, userid, the_follower):
        follower, created = cls.objects.get_or_create(
            userid=userid

        )
        follower.userid.remove(the_follower)
