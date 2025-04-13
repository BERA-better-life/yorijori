from rest_framework import serializers

class RecipeSerializer(serializers.Serializer):
    rcp_number = serializers.IntegerField()
    rcp_name = serializers.CharField(max_length=200)
    rcp_picture = serializers.CharField(max_length=500)
