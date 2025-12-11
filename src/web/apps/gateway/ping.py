from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([AllowAny])
def ping(request):
    logger.info(f"Ping endpoint called from {request.META.get('REMOTE_ADDR', 'unknown')}")
    logger.debug(f"Request method: {request.method}, Path: {request.path}")
    return Response("pong", status=status.HTTP_200_OK)
