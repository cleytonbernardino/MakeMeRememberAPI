from datetime import datetime

from django.contrib.auth import authenticate, get_user_model
from django.utils.timezone import get_current_timezone
from rest_framework.serializers import ValidationError

userModel = get_user_model()


def custom_validation(data):
    user = data['username'].strip()
    password = data['password'].strip()

    if not user or userModel.objects.filter(username=user).exists():
        raise ValidationError('Usuario já existe')

    if not password or len(password) < 8:
        raise ValidationError('A senha deve conter 8 caracteres no mínimo.')

    return data


def user_exist(username: str, password: str):
    return authenticate(
        username=username,
        password=password
    )


def user_validation(data):
    username = data['username']
    password = data['password']

    if not username:
        raise ValidationError("Usuario está em branco")

    if not password:
        raise ValidationError("Senha está em branco")

    if len(password) < 8:
        raise ValidationError("Senha deve conter 8 caracteres no mínimo")

    return data


def data_validation(data: str = None, time: str = None):
    if data is None or time is None or data == '' or time == '':
        return datetime.now(tz=get_current_timezone())

    data = data.split('/')
    time = time.split(':')
    try:
        data = [int(num) for num in data]
        time = [int(num) for num in time]
    except ValueError:
        return ValidationError("Data ou hora incorreta.")

    return datetime(
        day=data[0], month=data[1], year=data[2],
        hour=time[0], minute=time[1], second=0,
        tzinfo=get_current_timezone()
    )


def list_validation(data: dict, exist=False):
    title = data.get('title', None)
    content = data.get('content', None)
    priority = data.get('priority', 1)
    tag = data.get('tag', None)
    date = data.get('date', None)
    time = data.get('time', None)

    if not title or exist:
        raise ValidationError("Título incorreto ou já em uso.")

    if not content:
        raise ValidationError("Conteudo está vazio.")

    try:
        priority = int(priority)
        data['priority'] = priority
        if priority < 0 or priority > 10:
            data['priority'] = 1
    except ValueError:
        data['priority'] = 1

    if not tag:
        data['tag'] = 'Task'

    data['last_modification'] = data_validation(date, time)

    return data
