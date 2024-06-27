from random import choice
from string import ascii_letters

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.timezone import localtime
from rest_framework import serializers

from .models import TudoList

userModel = get_user_model()


def format_date(date):
    date = localtime(date)
    return date.strftime('%d/%m/%Y %H:%M')


class UserRegisterSerializer(serializers.Serializer):
    class Meta:
        model = userModel
        fields = ['usenarme', 'password']

    def password_hasher(self, password: str):
        chars = ascii_letters
        salt = ''.join(choice(chars) for _ in range(10))
        return make_password(password, salt)

    def create(self, clean_data: dict):
        password = make_password(clean_data['password'])
        user_obj = userModel.objects.create(
            username=clean_data['username'],
            password=password,
        )
        user_obj.save()
        return user_obj


class userSerializer(serializers.Serializer):
    class Meta:
        model = userModel
        fields = ('username', 'password')


class ListSerializer(serializers.Serializer):
    class Meta:
        model = TudoList
        fields = ('title', 'content')

    def create(self, user, clean_data: dict):
        obj = TudoList.objects.create(
            user=user,
            title=clean_data['title'],
            content=clean_data['content'],
            priority=clean_data['priority'],
            tag=clean_data['tag'],
            url_img=clean_data.get('url', 'None'),
            last_modification=clean_data['last_modification'],
            completed=False,
        )
        obj.save()
        return obj

    def get_task(self, user, id: int):
        try:
            task = TudoList.objects.get(
                user=user,
                pk=id
            )
            obj = {
                "id": task.pk,
                "title": task.title,
                "content": task.content,
                "priority": task.priority,
                "tag": task.tag,
                "url": task.url_img,
                "completed": task.completed,
                "dateTime": format_date(task.last_modification),
            }
            return obj
        except TudoList.DoesNotExist:
            return {
                'msg': f'Nenhuma Tarefa com o id: {id} foi encontrado.'
            }

    def get_all(self, user, completed=None):
        objs = []
        if completed is not None:
            tasks = TudoList.objects.filter(
                user=user, completed=completed
            ).order_by('-priority')
        else:
            tasks = TudoList.objects.filter(
                user=user
            ).order_by('-priority')

        for task in tasks:
            objs.append({
                "id": task.pk,
                "title": task.title,
                "content": task.content,
                "priority": task.priority,
                "tag": task.tag,
                "url": task.url_img,
                "completed": task.completed,
                "dateTime": format_date(task.last_modification),
            })
        return objs

    def update(self, user, id: int, clean_data: dict):
        try:
            item = TudoList.objects.get(
                user=user,
                pk=id
            )
        except TudoList.DoesNotExist:
            return None
        item.title = clean_data['title']
        item.content = clean_data['content']
        item.priority = clean_data['priority']
        item.tag = clean_data['tag']
        item.url_img = clean_data['url']
        item.completed = clean_data['completed']
        item.last_modification = clean_data['last_modification']
        item.save()
        return item

    def delete(self, user, id: int):
        try:
            task = TudoList.objects.get(
                user=user,
                pk=id
            )
            task.delete()
            return "Tarefa apagada com sucesso"
        except TudoList.DoesNotExist:
            raise ValueError("Tarefa não encontrada")

    def task_exist(self, user, title: str, id: int = 0):
        if title == '':
            return True

        try:
            exist = TudoList.objects.get(
                user=user,
                title=title
            )
            if id != 0:
                if exist.pk == id:
                    return False
            return True
        except TudoList.DoesNotExist:
            return False
