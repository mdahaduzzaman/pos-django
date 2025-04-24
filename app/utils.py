from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

def generate_jwt_for_user(user: User) -> dict:
    if user.is_authenticated:
        refresh = RefreshToken.for_user(user)

        return str(refresh.access_token)
    return None
