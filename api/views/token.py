from json import loads as json_loads

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import AccessToken

from api.serializer import UserRegisterSerializer
from api.validation import custom_validation, user_exist


@api_view(['POST'])
def login(request):
    username = request.data.get('username', None)
    password = request.data.get('password', None)

    user = user_exist(username, password)
    if not user:
        return Response({"msg": "Usuário ou senha inválida"}, status=400)

    return Response({
        "token": str(AccessToken.for_user(user)),
        "user": user.get_username()
    })


@api_view(['POST'])
def register(request):
    try:
        clean_data = custom_validation(request.data)
    except ValidationError as e:
        return Response({"msg": e.args[0]}, status=400)

    serializer = UserRegisterSerializer(data=clean_data)
    if serializer.is_valid(raise_exception=False):
        user = serializer.create(clean_data)
        if user:
            return Response({"msg": "Conta registrada com sucesso"}, status=201)  # noqa: E501
        return Response(status=400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    password = request.data.get('password', None)
    if not password:
        return Response({"msg": "Senha está em branco"}, status=400)

    serializer = UserRegisterSerializer()
    user = request.user

    hashed_password = serializer.password_hasher(password)
    user.password = hashed_password
    user.save()

    return Response({"msg": "Senha alterada com sucesso"})


# SWAGGER JSON
def loadjson(request):
    with open('api/doc/json_doc.json', 'r', encoding='utf8') as file:
        json_content = json_loads(file.read())

    return JsonResponse(
        json_content,
    )
