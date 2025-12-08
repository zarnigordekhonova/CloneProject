from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework.permissions import IsAuthenticated


class UserLogoutView(TokenBlacklistView):    
    pass


__all__ = [
    "UserLogoutView"
]