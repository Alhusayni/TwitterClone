# Generated by Django 2.2 on 2019-04-26 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twit', '0005_tweet_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Followers',
        ),
    ]
