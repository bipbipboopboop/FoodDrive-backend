from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

user = get_user_model()

class ShopUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = user
        fields = '__all__'