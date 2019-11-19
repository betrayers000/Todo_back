from django.shortcuts import render, get_object_or_404
from .models import Todo, User
from .serializers import TodoSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.http import JsonResponse, HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Create your views here.
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication, ))
def todo_create(request):
    serializer = TodoSerializer(data=request.POST)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
    return HttpResponse(status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication, ))
def todo_detail(request, id):
    todo = get_object_or_404(Todo, id=id)
    if request.method == "GET":
        serialiser = TodoSerializer(todo)
        return JsonResponse(serialiser.data)
    elif request.method == "PUT":
        serialiser = TodoSerializer(todo, data=request.data)
        if serialiser.is_valid():
            serialiser.save()
            return JsonResponse(serialiser.data)
        return HttpResponse(status=400)
    elif request.method == "DELETE":
        todo.delete()
        return JsonResponse({'msg': 'delete'})


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication, ))
def user_detail(request, id):
    user = get_object_or_404(User, id=id)
    if request.user != user:
        return HttpResponse(status=404)
    if request.method == "GET":
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)