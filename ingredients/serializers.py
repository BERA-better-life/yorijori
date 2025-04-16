from rest_framework import serializers
from .models import UserIngredients, ExcludedIngredients

class UserIngredientsSerializer(serializers.ModelSerializer):
    expiration_date = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = UserIngredients
        fields = ['user_ingredient_id', 'user_id', 'ingredient_id', 'expiration_date']
        read_only_fields = ['user_ingredient_id', 'user_id']

    def validate_expiration_date(self, value):
        from datetime import date
        if value and value < date.today():
            raise serializers.ValidationError({"error": "유효한 날짜값을 입력하세요."})
        return value

class ExcludedIngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcludedIngredients
        fields = ['excluded_id', 'user_id', 'ingredient']
        read_only_fields = ['excluded_id', 'user_id']
