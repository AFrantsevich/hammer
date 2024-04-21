from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class MyBackend(ModelBackend):
    def authenticate(self, request, username=None,
                     password=None, phone=None,
                     otp=None, **kwargs):
        UserModel = get_user_model()
        if username:
            try:
                user = UserModel.objects.get(username=username)
                user.check_password(password) and self.user_can_authenticate(user)
                return user
            except Exception:
                return None
        elif phone:
            try:
                user = UserModel.objects.get(phone=phone)
            except UserModel.DoesNotExist:
                return None
            else:
                if user.otp == otp:
                    user.otp = None
                    user.save()
                    return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
