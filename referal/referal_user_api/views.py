from django.contrib.auth import authenticate


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token


from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


from referal_user.utils import (otp_authenticator,
                                set_personal_referral_code,
                                referral_code_validator,
                                create_or_get_user, clean_data)
from referal_user.models import CustomUser


from .serializers import (UserSerializer,
                          PhoneReferralCodeSerializer, UserAuthSerializer)


class LoginWithOTP(APIView):
    permission_classes = ([AllowAny])
    authentication_classes = []

    @swagger_auto_schema(
            request_body=PhoneReferralCodeSerializer,
            responses={
                status.HTTP_200_OK: 'OTP has been sent to your phone.',
                status.HTTP_400_BAD_REQUEST: "Bad Request. Validate Error"
            },
        security=authentication_classes
        )
    def post(self, request):

        user_data = PhoneReferralCodeSerializer(data=request.data)
        if not user_data.is_valid():
            return Response(user_data.errors, status=status.HTTP_400_BAD_REQUEST)

        phone = user_data.validated_data.pop('phone')
        referral_code = user_data.validated_data.get('referral_code', None)

        context, user = create_or_get_user(phone)

        context.update(referral_code_validator(referral_code, user))

        if context:
            clean_data(user)
            return Response(data=context, status=status.HTTP_400_BAD_REQUEST)

        otp_authenticator(user=user, phone=phone)

        return Response({'message': 'OTP has been sent to your phone.'},
                        status=status.HTTP_200_OK)


class ValidateOTP(APIView):

    @swagger_auto_schema(
            request_body=UserAuthSerializer,
            responses={
                status.HTTP_200_OK: 'Token',
                status.HTTP_400_BAD_REQUEST: "Invalid_credentials"
            },
        )
    def post(self, request):
        credentials = UserAuthSerializer(data=request.data)
        credentials.is_valid()

        phone = credentials.validated_data.get('phone', '!')
        otp = credentials.validated_data.get('otp', '!')

        user = authenticate(request, phone=phone, otp=otp)
        if user:
            token = Token.objects.create(user=user)

            set_personal_referral_code(user)

            return Response({'Token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid_credentials'},
                        status=status.HTTP_400_BAD_REQUEST)


class UserProfile(APIView):
    permission_classes = ([IsAuthenticated])

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: UserSerializer()},
        manual_parameters=[
            openapi.Parameter(name="Token",
                              in_=openapi.IN_HEADER,
                              type=openapi.TYPE_STRING,
                              required=True,
                              description="Token Authentication",
                              default='Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b')
                           ],
        )
    def get(self, request):
        queryset = CustomUser.objects.select_related(
            'referral_code').get(pk=request.user.id)
        serialized = UserSerializer(queryset)
        return Response(serialized.data, status=status.HTTP_200_OK)
