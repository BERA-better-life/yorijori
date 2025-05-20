from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response
from datetime import timedelta, date
from ingredients.models import UserIngredients
from users.models import Users
import requests

EXPO_PUSH_URL = "https://exp.host/--/api/v2/push/send"

@api_view(['POST'])
def send_expiration_notifications(request):
    today = date.today()
    target_date = today + timedelta(days=7)


    user_ingredients = UserIngredients.objects.select_related('user_id', 'ingredient_id').filter(
    expiration_date__range=(today, target_date)
    )

    notified_users = {}

    for ui in user_ingredients:
        user = ui.user_id
        ingredient = ui.ingredient_id

        if not user.expo_push_token:
            continue

        if user.user_id not in notified_users:
            notified_users[user.user_id] = {
                "token": user.expo_push_token,
                "ingredients": []
            }

        notified_users[user.user_id]["ingredients"].append(ingredient.ingredient_name)

    for user_id, info in notified_users.items():
        ingredients_list = ', '.join(info['ingredients'])
        message = f"다음 재료의 유통기한이 7일 이내예요: {ingredients_list}"

        payload = {
            "to": info["token"],
            "sound": "default",
            "title": "⏰ 유통기한 알림",
            "body": message
        }

        response = requests.post(EXPO_PUSH_URL, json=payload)
        print(f"유저 {user_id}에게 알림 전송됨: {response.status_code} - {response.text}")

    return Response({"message": "알림 전송 완료", "total_users": len(notified_users)})
