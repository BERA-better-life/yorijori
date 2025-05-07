from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from favorite.models import Likes
from recipes.models import Recipes
from users.models import Users

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, recipe_id):
    user = request.user
    try:
        recipe = Recipes.objects.get(pk=recipe_id)
    except Recipes.DoesNotExist:
        return Response({"error": "Recipe not found."}, status=404)

    like, created = Likes.objects.get_or_create(user_id=user, rcp_number=recipe)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    like_count = Likes.objects.filter(rcp_number=recipe).count()

    return Response({
        "liked": liked,
        "like_count": like_count
    })

from .serializers import LikesSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liked_recipes(request):
    likes = Likes.objects.filter(user_id=request.user)
    serializer = LikesSerializer(likes, many=True)
    return Response(serializer.data)
