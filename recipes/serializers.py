from rest_framework import serializers

class IngredientInputSerializer(serializers.Serializer):
    ingredients = serializers.CharField(help_text="입력 재료들을 쉼표로 구분한 문자열")

class IngredientInputSerializer(serializers.Serializer):
    ingredients = serializers.CharField()
    excluded_ingredients = serializers.CharField(required=False, allow_blank=True)