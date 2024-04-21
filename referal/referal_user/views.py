from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


from referal_user.models import CustomUser


from .utils import (set_personal_referral_code,
                    referral_code_validator,
                    create_or_get_user, clean_data)


def login_request(request: HttpRequest):
    user = None
    phone = request.POST.get('phone', None)
    referral_code = request.POST.get('referral_code', None)

    context = {}

    if phone:
        context, user = create_or_get_user(phone, request)
        context.update(context)

    if referral_code and user:
        context.update(referral_code_validator(referral_code, user))

    if not context and phone:
        return redirect('referal_user:auth', )

    clean_data(user)

    return render(request, 'referal_user/login.html', context=context)


def authenticate_user(request: HttpRequest):
    context = {}

    phone = request.session.get('phone', None)
    otp = request.POST.get('otp', None)

    if otp and phone:
        user = authenticate(request, phone=phone, otp=otp)
        if user:
            set_personal_referral_code(user)
            login(request, user)
            return redirect('referal_user:user_info')

        context.update({'error': 'Sorry, wrong code'})

    return render(request, 'referal_user/auth.html', context=context)


@login_required
def user_info(request: HttpRequest):
    queryset = CustomUser.objects.select_related(
        'referral_code').get(pk=request.user.id)
    context = {
        'queryset': queryset
    }

    return render(request, 'referal_user/user_info.html',
                  context=context)


def get_code(request: HttpRequest):

    context = {}
    phone = request.POST.get('phone', None)
    if phone:
        code = CustomUser.objects.get(phone=phone).otp

        context.update({
            'code': code
        })

    return render(request, 'referal_user/code.html', context)