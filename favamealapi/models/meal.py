from django.db import models
from django.contrib.auth.models import User
from .mealrating import MealRating

class Meal(models.Model):

    name = models.CharField(max_length=55)
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE)
    favs = models.ManyToManyField(User,
                                  through="FavoriteMeal",
                                  related_name="favorite_meals")

    # TODO: Add a `favorite` custom property
    @property
    def favorite(self):
        return self.__favorite

    @favorite.setter
    def favorite(self, value):
        self.__favorite = value
    # TODO: Add an user_rating custom properties

    @property
    def user_rating(self):
        return self.__user_rating

    @user_rating.setter
    def user_rating(self, value):
        self.__user_rating = value

    # TODO: Add an avg_rating custom properties
    @property
    def avg_rating(self):
        return self.__avg_rating

    @avg_rating.setter
    def avg_rating(self, value):
        self.__avg_rating = value