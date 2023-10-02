from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "uuid",
            "email",
            "password",
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["email"],
            validated_data["password"]
        )

        return user
