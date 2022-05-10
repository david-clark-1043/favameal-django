# Generated by Django 3.1.3 on 2022-05-10 19:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('favamealapi', '0002_auto_20201116_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='favs',
            field=models.ManyToManyField(related_name='favorite_meals', through='favamealapi.FavoriteMeal', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='favs',
            field=models.ManyToManyField(related_name='favorite_restaurants', through='favamealapi.FavoriteRestaurant', to=settings.AUTH_USER_MODEL),
        ),
    ]
