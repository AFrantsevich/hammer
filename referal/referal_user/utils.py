import random
import string
import re


from django.utils.crypto import get_random_string
from django.db import IntegrityError


from referal_user.models import CustomUser


def generate_otp(length):
    characters = string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp


def send_otp_phone(phone_number, otp):
    pass


def otp_authenticator(user, phone):
    try:
        otp = generate_otp(4)

        setattr(user, 'otp', otp)
        user.save()
        send_otp_phone(phone, otp)

    except Exception:
        return Exception


def set_personal_referral_code(user):
    try:
        if getattr(user, 'personal_referral_code'):
            return
        setattr(user, 'personal_referral_code', get_random_string(6))
        user.save()
    except IntegrityError as e:
        if 'unique constraint' in str(e.args).lower():
            set_personal_referral_code(user)
        else:
            raise e


def phone_validator(phone):
    valid_func = re.compile(r"^\+7(?:\d{3}){2}(?:\d{2}){2}$")
    if valid_func.match(phone):
        return True
    return False


def referral_code_exist_validator(code, user):
    code_exist = CustomUser.objects.filter(
        personal_referral_code=code).exists()
    code_user = CustomUser.objects.get(pk=user.id).referral_code
    if code_user:
        code_user = code_user.personal_referral_code
    return (code_exist and (code_user is None)), code_user


def referral_code_validator(referral_code, user):
    context = {}

    if not referral_code:
        return context

    result, code_user = referral_code_exist_validator(referral_code, user)
    if result:
        setattr(user, 'referral_code',
                CustomUser.objects.filter(
                    personal_referral_code=referral_code).first())
        user.save()
    else:
        if code_user:
            context.update({'error_code': f"You already have code {code_user}"})
        else:
            context.update({'error_code': f"Sorry, code doesn't exist"})
    return context


def create_or_get_user(phone, request=None):
    user = None
    context = {}
    if phone_validator(phone):
        user, created = CustomUser.objects.get_or_create(
            phone=phone, username=phone)
        otp_authenticator(user=user, phone=phone)
        if request:
            request.session.update({'phone': phone})
    else:
        context.update({'error': 'Invalid data. Format +78883332211'})
    return context, user


def clean_data(user):
    if user:
        setattr(user, 'otp', None)
        user.save()
