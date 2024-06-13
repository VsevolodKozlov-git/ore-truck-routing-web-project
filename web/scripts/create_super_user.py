from django.contrib.auth.models import User
from utils.utils import get_env_variable


def run():
    username = get_env_variable("DJANGO_SUPERUSER_USERNAME")
    password = get_env_variable("DJANGO_SUPERUSER_PASSWORD")
    user = User.objects.create_user(username, password=password)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print("Created superuser")
