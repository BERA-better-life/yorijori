from rest_framework import serializers
from .models import UserIngredients, ExcludedIngredients

class UserIngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIngredients
        fields = ['user_ingredient_id', 'user_id', 'ingredient_id', 'expiration_date'] #"ingredient > ingredient_id로 수정 0503 wh
        read_only_fields = ['user_ingredient_id', 'user_id']

class ExcludedIngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcludedIngredients
        fields = ['excluded_id', 'user_id', 'ingredient_id'] #"ingredient > ingredient_id로 수정 0503 wh
        read_only_fields = ['excluded_id', 'user_id']
