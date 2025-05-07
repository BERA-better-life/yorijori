from rest_framework import serializers
from .models import Likes

class LikesSerializer(serializers.ModelSerializer):
    recipe_id = serializers.IntegerField(source='rcp_number.rcp_number')
    recipe_title = serializers.CharField(source='rcp_number.rcp_name')

    class Meta:
        model = Likes
        fields = ['recipe_id', 'recipe_title']