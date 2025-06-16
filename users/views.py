from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .serializers import PatientSerializer, DoctorSerializer, AdminSerializer
from .services import _get_patient_by_login, _get_doctor_by_login, _get_admin_by_login
from .models import User
from mis.settings import ROLE_CHOICES


class RegistrationPatientAPIView(APIView):

    def post(self, request):

        if not validate_role_id(request.data):
            return Response({
                "Invalid role name"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = PatientSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "Error": serializer.errors
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user = serializer.save()

        tokens = get_tokens(user)

        return Response({
            'refresh': str(tokens),
            'access': str(tokens.access_token),
        }, status=status.HTTP_201_CREATED)


class LoginPatientAPIView(APIView):

    def post(self, request):

        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({'error': 'Password and username are required'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = _get_patient_by_login(username=username, password=password)

        if user is None:
            return Response({'error': 'Username or password are incorrect'},
                            status=status.HTTP_401_UNAUTHORIZED)

        tokens = get_tokens(user)

        return Response({
            'refresh': str(tokens),
            'access': str(tokens.access_token),
        }, status=status.HTTP_200_OK)


class RegistrationDoctorAPIView(APIView):

    def post(self, request):

        if not validate_role_id(request.data):
            return Response({
                "Invalid role name"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = DoctorSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "Error": serializer.errors
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user = serializer.save()

        tokens = get_tokens(user)

        return Response({
            'refresh': str(tokens),
            'access': str(tokens.access_token),
        }, status=status.HTTP_201_CREATED)


class LoginDoctorAPIView(APIView):

    def post(self, request):

        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({'error': 'Password and username are required'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = _get_doctor_by_login(username=username, password=password)

        if user is None:
            return Response({'error': 'Username or password are incorrect'},
                            status=status.HTTP_401_UNAUTHORIZED)

        tokens = get_tokens(user)

        return Response({
            'refresh': str(tokens),
            'access': str(tokens.access_token),
        }, status=status.HTTP_200_OK)


class RegistrationAdminAPIView(APIView):

    def post(self, request):

        if not validate_role_id(request.data):
            return Response({
                "Invalid role name"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = AdminSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "Error": serializer.errors
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user = serializer.save()

        tokens = get_tokens(user)

        return Response({
            'refresh': str(tokens),
            'access': str(tokens.access_token),
        }, status=status.HTTP_201_CREATED)


class LoginAdminAPIView(APIView):

    def post(self, request):

        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({'error': 'Password and username are required'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = _get_admin_by_login(username=username, password=password)

        if user is None:
            return Response({'error': 'Username or password are incorrect'},
                            status=status.HTTP_401_UNAUTHORIZED)

        tokens = get_tokens(user)

        return Response({
            'refresh': str(tokens),
            'access': str(tokens.access_token),
        }, status=status.HTTP_200_OK)


def validate_role_id(data: dict) -> bool:
    role_id = data.get("role")
    if role_id is None:
        return False

    if ROLE_CHOICES.get(role_id) is None:
        return False

    return True


def get_tokens(user: User) -> RefreshToken:
    refresh = RefreshToken.for_user(user)

    refresh.payload.update({
        'user_id': user.id,
        'role': user.role,
    })

    return refresh
