from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import Task
from .serializers import TaskSerializer, UserSerializer


# ----------------------------------
# REGISTER USER
# ----------------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "message": "User registered successfully",
            "token": token.key
        }, status=201)

    return Response(serializer.errors, status=400)


# ----------------------------------
# LOGIN USER
# ----------------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "message": "Login successful",
            "token": token.key
        })
    else:
        return Response({
            "error": "Invalid credentials"
        }, status=400)


# ----------------------------------
# GET LOGGED-IN USER TASKS
# ----------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_tasks(request):
    tasks = Task.objects.filter(user=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


# ----------------------------------
# UPDATE TASK STATUS
# ----------------------------------
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task_status(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    task.status = request.data.get('status', task.status)
    task.save()

    serializer = TaskSerializer(task)
    return Response(serializer.data)
