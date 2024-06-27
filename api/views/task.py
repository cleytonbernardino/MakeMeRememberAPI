from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from api.serializer import ListSerializer
from api.validation import list_validation


class Tasks(APIView):
    permission_classes = (IsAuthenticated, )
    serializer = ListSerializer()

    def get(self, request, id: int = 0):
        completed = request.GET.get('completed', None)
        if completed is not None:
            completed = True if completed == 'true' else False

        if id == 0:
            data = self.serializer.get_all(
                request.user, completed
            )
            return Response(data)

        item = self.serializer.get_task(user=request.user, id=id)
        return Response(item)

    def post(self, request):
        try:
            exist = self.serializer.task_exist(
                    request.user, request.data.get('title', '')
                )
            clean_data = list_validation(request.data, exist)
        except ValidationError as e:
            return Response({"msg": e.args[0]}, status=400)

        tlist = self.serializer.create(request.user, clean_data)
        if tlist:
            return Response({"msg": "Tarefa criada com sucesso"}, status=201)  # noqa: E501
        return Response({"msg", "Erro ao criar a tarefa"}, status=400)

    def put(self, request, id: int):
        try:
            exist = self.serializer.task_exist(
                request.user, request.data.get('title', ''), id
            )
            clean_data = list_validation(request.data, exist)
        except ValidationError as e:
            return Response({"msg": e.args[0]}, status=400)

        item = self.serializer.update(request.user, id, clean_data)
        if item:
            return Response({"msg": "Tarefa atualizada com sucesso"})  # noqa: E501

        return Response(
            {'msg': 'Não foi possível atualizar a tarefa'}, status=400
        )

    def delete(self, request, id: int):
        try:
            task = self.serializer.delete(
                user=request.user,
                id=id
            )
            return Response({"msg": task})
        except ValueError as err:
            return Response(
                {"msg": str(err)}, status=404
            )
