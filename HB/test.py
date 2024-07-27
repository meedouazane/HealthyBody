import django
import os
from django.db import IntegrityError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HB.settings")
django.setup()

from django.contrib.auth import get_user_model
from bmi.models import Records
CustomUser = get_user_model()


def create_user(username, email, password, sex, date_of_birth):
    """ Create user Func """
    try:
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            sex=sex,
            date_of_birth=date_of_birth
        )
        print(f"User '{username}' created successfully.")
        return user
    except IntegrityError:
        print('This User Already exist')


def get_user(username):
    """ get user by username """
    user = CustomUser.objects.get(username=username)
    return user


def get_bmi(username):
    """ get bmi for specific user """
    user = get_user(username)
    rec = Records.objects.filter(user_id=user).values().all()
    return rec


def create_bmi(weight, height, username):
    """ add bmi for a user """
    height = height / 100
    bmi = weight / (height * height)
    bmi = round(bmi, 2)
    try:
        user = get_user(username)
        rec = Records.objects.create(
            weight=weight,
            height=height,
            bmi=bmi,
            user_id=user
        )
        return rec
    except Exception as e:
        return print(e)


# re = get_bmi(username='heroKami')
# for b in re:
#     print(b.get('bmi'))
create_bmi(username='hellow', weight=66, height=174)




