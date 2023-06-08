from typing import Dict
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def create_jwt_pair_for_user(user: User):
    """
    Obtains pairs of tokens ie ( access and refresh for the user)
    :param ::: user >> an object of the user to create token for
    """
    refresh = RefreshToken.for_user(user)

    tokens = {"access": str(refresh.access_token), "refresh": str(refresh)}

    return tokens


