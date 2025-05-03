from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    """
    Возвращает текущего залогиненного пользователя:
    {
      "id": <int>,
      "role": "manager" или "admin"
    }
    """
    user = request.user
    return Response({
        'id': user.id,
        'role': user.role,
    })