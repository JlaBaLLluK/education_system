from django.contrib.auth import authenticate, login, logout
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView

from student.serializers import StudentSerializer, LoginSerializer


class RegistrationView(CreateAPIView):
    serializer_class = StudentSerializer


class LoginView(APIView):
    serializer_class = LoginSerializer

    @staticmethod
    def post(request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        user = authenticate(username=serializer.data.get('username'), password=serializer.data.get('password'))
        if user is None:
            return Response({'error': 'Wrong credentials!'}, status=HTTP_400_BAD_REQUEST)

        login(request, user)
        return Response({'success': 'Login successful!'}, status=HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        logout(request)
        return Response({'success': 'Logout successful!'}, status=HTTP_200_OK)
