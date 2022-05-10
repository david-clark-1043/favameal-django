"""View module for handling requests about restaurants"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User
from favamealapi.models import Restaurant
from favamealapi.models.favoriterestaurant import FavoriteRestaurant
from rest_framework.decorators import action


class RestaurantSerializer(serializers.ModelSerializer):
    """JSON serializer for restaurants"""

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'address', 'favs', 'favorite')

        # TODO: Add 'favorite' field to RestaurantSerializer

class FaveSerializer(serializers.ModelSerializer):
    """JSON serializer for favorites"""

    class Meta:
        model = FavoriteRestaurant
        fields = ('restaurant',)
        depth = 1


class RestaurantView(ViewSet):
    """ViewSet for handling restuarant requests"""

    def create(self, request):
        """Handle POST operations for restaurants

        Returns:
            Response -- JSON serialized event instance
        """
        rest = Restaurant()
        rest.name = request.data["name"]
        rest.address = request.data["address"]

        try:
            rest.save()
            serializer = RestaurantSerializer(
                rest, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            restaurant = Restaurant.objects.get(pk=pk)

            # TODO: Add the correct value to the `favorite` property of the requested restaurant
            user = User.objects.get(user=request.auth.user)
            restaurant.favorite = user in restaurant.favs.all()
            
            serializer = RestaurantSerializer(
                restaurant, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to restaurants resource

        Returns:
            Response -- JSON serialized list of restaurants
        """
        restaurants = Restaurant.objects.all()

        # TODO: Add the correct value to the `favorite` property of each restaurant
        user = User.objects.get(pk=request.auth.user_id)
        # Set the `joined` property on every event
        for restaurant in restaurants:
            # Check to see if the user is in the attendees list on the event
            restaurant.favorite = user in restaurant.favs.all()

        serializer = RestaurantSerializer(restaurants, many=True, context={'request': request})

        return Response(serializer.data)

    # TODO: Write a custom action named `star` that will allow a client to
    # send a POST and a DELETE request to /restaurant/2/star
    @action(methods=['post'], detail=True)
    def star(self, request, pk):
        """Post request for a user to sign up for an event"""
    
        user = User.objects.get(pk=request.auth.user_id)
        restaurant = Restaurant.objects.get(pk=pk)
        restaurant.favs.add(user) # for list .add(*gamerArray)
        return Response({'message': 'Favorite added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def unstar(self, request, pk):
        """Post request for a user to sign up for an event"""
    
        user = User.objects.get(pk=request.auth.user_id)
        restaurant = Restaurant.objects.get(pk=pk)
        restaurant.favs.remove(user) # for list .add(*gamerArray)
        return Response({'message': 'favorite removed'}, status=status.HTTP_204_NO_CONTENT)