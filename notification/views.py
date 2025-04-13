from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth import get_user_model
from ingredients.models import UserIngredient

User = get_user_model()

@require_GET
def expiration_alerts_view(request, user_id):
    today = timezone.now().date()
    deadline = today + timedelta(days=3)

    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    items = UserIngredient.objects.filter(
        user=user,
        expiration_date__range=(today, deadline)
    ).select_related("ingredient")

    result = [
        {
            "ingredient_name": i.ingredient.ingredient_name,
            "expiration_date": str(i.expiration_date),
            "days_left": (i.expiration_date - today).days,
        }
        for i in items
    ]

    return JsonResponse({"alerts": result})