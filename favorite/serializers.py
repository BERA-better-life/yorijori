from rest_framework import serializers
from .models import Likes, Bookmarks

class LikesSerializer(serializers.ModelSerializer):
    recipe_id = serializers.IntegerField(source='rcp_number.rcp_number')
    recipe_title = serializers.CharField(source='rcp_number.rcp_name')

    class Meta:
        model = Likes
        fields = ['recipe_id', 'recipe_title']

class BookmarksSerializer(serializers.ModelSerializer):
    recipe_id = serializers.IntegerField(source='rcp_number_id')
    recipe_title = serializers.CharField(source='rcp_number.rcp_name')

    class Meta:
        model = Bookmarks
        fields = ['recipe_id', 'recipe_title']