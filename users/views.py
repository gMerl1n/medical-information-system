from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .serializers import PatientSerializer
from .services import _get_user_by_login
from mis.settings import ROLE_CHOICES


class RegistrationAPIView(APIView):

    def post(self, request):

        if not self.validate_role_id(request.data):
            return Response({
                "Invalid role id"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = PatientSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "Invalid data"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        refresh.payload.update({
            'user_id': user.id,
            'role_id': user.role_id,
        })

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

    @staticmethod
    def validate_role_id(data: dict) -> bool:
        role_id = data.get("role_id")
        if role_id is None:
            return False

        if ROLE_CHOICES.get(role_id) is None:
            return False

        return True

class LoginAPIView(APIView):

    def post(self, request):

        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({'error': 'Password and username are required'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = _get_user_by_login(username=username, password=password)

        if user is None:
            return Response({'error': 'Username or password are incorrect'},
                            status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        refresh.payload.update({
            'user_id': user.id,
            'username': user.username

        })

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)