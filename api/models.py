from django.contrib.auth.models import User
from django.db import models


class TudoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Título', max_length=50)
    content = models.TextField('Conteudo', max_length=255)
    priority = models.IntegerField('Prioridade', default=1)
    tag = models.CharField('Tag', default="Task", max_length=15)
    url_img = models.URLField('URL da imagem', blank=True)
    completed = models.BooleanField('Concluido', default=False)
    last_modification = models.DateTimeField()

    def __str__(self):
        return f'{self.user.username} ({self.title})'
