from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import DoorOrderSerializer


class DoorOrderCreateAPIView(GenericAPIView):
    serializer_class = DoorOrderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        return Response(self.get_serializer(order).data, status=status.HTTP_201_CREATED)
    


__all__ = [
    "DoorOrderCreateAPIView"
]

