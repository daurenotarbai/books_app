from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from django.core.exceptions import ObjectDoesNotExist

from .models import VerificationCode
from .serializers import TokenObtainPairsSerializer, UserSerializer, VerificationCodeSerializer
from auth.utils import send_code_for_verify
from core.exceptions import InvalidCode
from users.models import User


class SignInView(TokenObtainPairView):
    serializer_class = TokenObtainPairsSerializer


@permission_classes((AllowAny,))
class SingUpView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializer.validated_data
        send_code_for_verify(user)
        return Response(data, status=status.HTTP_201_CREATED)


@permission_classes((AllowAny,))
class EmailVerifyView(GenericAPIView):
    serializer_class = VerificationCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        try:
            verification_code = VerificationCode.objects.get(code=code, email=email)
        except ObjectDoesNotExist:
            raise InvalidCode
        else:
            user = User.objects.get(email=verification_code.email)
            user.is_verified = True
            user.save()
            verification_code.delete()
            return Response('User successfully verified', status=status.HTTP_200_OK)