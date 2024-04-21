from referal_user.models import CustomUser
from rest_framework import serializers
from referal_user.utils import phone_validator


class UserSerializer(serializers.ModelSerializer):

    my_referral_users = serializers.StringRelatedField(many=True)

    class Meta:
        model = CustomUser
        fields = ('phone', 'my_referral_users', 'personal_referral_code')


class PhoneReferralCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=12, min_length=12)
    referral_code = serializers.CharField(max_length=6,
                                          required=False,
                                          min_length=6)

    def validate(self, data):
        referral_code = data.get('referral_code', None)
        if referral_code:
            if not CustomUser.objects.filter(
                    personal_referral_code=referral_code).exists():
                raise serializers.ValidationError({
                    'error': "This referral_code doesn't exist"})

        phone = data.get('phone', None)

        if not phone_validator(phone):
            raise serializers.ValidationError({
                'error': "Invalid number. Must be +70000000000"})

        return data


class UserAuthSerializer(PhoneReferralCodeSerializer, serializers.ModelSerializer):
    otp = serializers.CharField(max_length=4, min_length=4, required=True)

    class Meta:
        model = CustomUser
        fields = ('phone', 'otp')
