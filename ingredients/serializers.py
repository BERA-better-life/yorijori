from rest_framework import serializers
from .models import UserIngredients, ExcludedIngredients, Ingredients

class UserIngredientsSerializer(serializers.ModelSerializer):
    expiration_date = serializers.DateField(required=False, allow_null=True)
    ingredient_name = serializers.SerializerMethodField()

    class Meta:
        model = UserIngredients
        fields = ['user_ingredient_id', 'user_id', 'ingredient_id', 'ingredient_name', 'expiration_date']
        read_only_fields = ['user_ingredient_id', 'user_id']

    def get_ingredient_name(self, obj):
        if obj.ingredient_id:
            return obj.ingredient_id.ingredient_name
        return None

    def validate_expiration_date(self, value):
        from datetime import date
        if value and value < date.today():
            raise serializers.ValidationError({"error": "유효한 날짜값을 입력하세요."})
        return value

class ExcludedIngredientsSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.SerializerMethodField()

    class Meta:
        model = ExcludedIngredients
        fields = ['excluded_id', 'user_id', 'ingredient_id', 'ingredient_name']
        read_only_fields = ['excluded_id', 'user_id']

    def get_ingredient_name(self, obj):
        if obj.ingredient_id:
            return obj.ingredient_id.ingredient_name
        return None

class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = '__all__'
