"""View module for handling requests about meals"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from favamealapi.models import Meal, MealRating, Restaurant, FavoriteMeal
from favamealapi.views.restaurant import RestaurantSerializer
from django.contrib.auth.models import User


class MealSerializer(serializers.ModelSerializer):
    """JSON serializer for meals"""
    restaurant = RestaurantSerializer(many=False)

    class Meta:
        model = Meal
        fields = ('id', 'name', 'restaurant', 'favorite', 'user_rating', 'avg_rating')

        # TODO: Add 'user_rating', 'avg_rating' fields to MealSerializer

class MealRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealRating
        fields = ('rating', )



class MealView(ViewSet):
    """ViewSet for handling meal requests"""

    def create(self, request):
        """Handle POST operations for meals

        Returns:
            Response -- JSON serialized meal instance
        """
        meal = Meal()
        meal.name = request.data["name"]
        meal.restaurant = Restaurant.objects.get(pk=request.data["restaurant_id"])


        try:
            meal.save()
            serializer = MealSerializer(
                meal, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single meal

        Returns:
            Response -- JSON serialized meal instance
        """
        try:
            meal = Meal.objects.get(pk=pk)

            # TODO: Get the rating for current user and assign to `user_rating` property
            user = User.objects.get(pk=request.auth.user_id)
            
            meal_ratings = MealRating.objects.filter(meal=meal)
            user_rating = 0
            for obj in meal_ratings:
                if obj.user == user:
                    user_rating = obj.rating
            if user_rating:
                meal.user_rating = user_rating
            else:
                meal.user_rating = "No rating"
            # TODO: Get the average rating for requested meal and assign to `avg_rating` property
            if(len(meal_ratings) == 0):
                meal.avg_rating = "No meal ratings"
            else:
                # Sum all of the meal_ratings for the game
                total_rating = 0
                for rating in meal_ratings:
                    total_rating += rating.rating

                # Calculate the average and return it.
                
                average = total_rating / len(meal_ratings)
                meal.avg_rating = average
            # TODO: Assign a value to the `is_favorite` property of requested meal
            meal.favorite = user in meal.favs.all()

            serializer = MealSerializer(
                meal, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to meals resource

        Returns:
            Response -- JSON serialized list of meals
        """
        meals = Meal.objects.all()
        meal_ratings = MealRating.objects.all()

        # TODO: Get the rating for current user and assign to `user_rating` property
        user = User.objects.get(pk=request.auth.user_id)
        
        for meal in meals:
            meal_ratings = MealRating.objects.filter(meal=meal)
            user_rating = 0
            for obj in meal_ratings:
                if obj.user == user:
                    user_rating = obj.rating
            if user_rating:
                meal.user_rating = user_rating
            else:
                meal.user_rating = "No rating"
    
        # TODO: Get the average rating for each meal and assign to `avg_rating` property
            if(len(meal_ratings) == 0):
                meal.avg_rating = "No meal ratings"
            else:
                # Sum all of the meal_ratings for the game
                total_rating = 0
                for rating in meal_ratings:
                    total_rating += rating.rating

                # Calculate the average and return it.
                
                average = total_rating / len(meal_ratings)
                meal.avg_rating = average
            
            meal.favorite = user in meal.favs.all()
            
                # If you don't know how to calculate average, Google it.
        # TODO: Assign a value to the `is_favorite` property of each meal

        serializer = MealSerializer(
            meals, many=True, context={'request': request})

        return Response(serializer.data)

    # TODO: Add a custom action named `rate` that will allow a client to send a
    #  POST and a PUT request to /meals/3/rate with a body of..
    #       {
    #           "rating": 3
    #       }
    @action(methods=('post', 'put'), detail=True)
    def rate(self, request, pk):
        if request.method.lower() == "post":
            user = User.objects.get(pk=request.auth.user_id)
            meal = Meal.objects.get(pk=pk)
            mrs = MealRating.objects.all()
            update_mr = None
            for mr in mrs:
                if mr.meal == meal and mr.user == user:
                    update_mr = mr
            
            if update_mr is None:
                serializer = MealRatingSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(user=user, meal=meal)
                
                return Response({'message': 'rating added'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': "rating already given, update rating instead"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        elif request.method.lower() == "put":
            user = User.objects.get(pk=request.auth.user_id)
            meal = Meal.objects.get(pk=pk)
            mrs = MealRating.objects.all()
            update_mr = None
            for mr in mrs:
                if mr.meal == meal and mr.user == user:
                    update_mr = mr
            
            serializer = MealRatingSerializer(update_mr, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'rating updated'}, status=status.HTTP_204_NO_CONTENT)

    # TODO: Add a custom action named `star` that will allow a client to send a
    #  POST and a DELETE request to /meals/3/star.
    @action(methods=('post', 'delete'), detail=True)
    def star(self, request, pk):
        if request.method.lower() == "post":
            """Post request for a user to sign up for an event"""
        
            user = User.objects.get(pk=request.auth.user_id)
            restaurant = Restaurant.objects.get(pk=pk)
            restaurant.favs.add(user) # for list .add(*gamerArray)
            return Response({'message': 'Favorite added'}, status=status.HTTP_201_CREATED)
        elif request.method.lower() == "delete":
            """Post request for a user to sign up for an event"""
        
            user = User.objects.get(pk=request.auth.user_id)
            restaurant = Restaurant.objects.get(pk=pk)
            restaurant.favs.remove(user) # for list .add(*gamerArray)
            return Response({'message': 'favorite removed'}, status=status.HTTP_204_NO_CONTENT)