from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
import logging

logger = logging.getLogger(__name__)


@permission_classes([AllowAny])
def ping(request):
    logger.info(f"Ping endpoint called from {request.META.get('REMOTE_ADDR', 'unknown')}")
    logger.debug(f"Request method: {request.method}, Path: {request.path}")
    return JsonResponse("pong", safe=False, status=status.HTTP_200_OK)
