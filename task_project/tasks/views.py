from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer, UserSerializer
from django.contrib.auth.models import User
from django.utils.timezone import now
from .models import UserActivity
from rest_framework.permissions import IsAdminUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User registered successfully'})
    return Response(serializer.errors, status=400)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return JsonResponse({
                'token': token.key,
                'is_admin': user.is_superuser  # or user.is_staff
            })
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_tasks(request):
    user = request.user
    tasks = Task.objects.filter(assignee=user)
    serializer = TaskSerializer(tasks, many=True)
    return Response({"username": user.username, "tasks": serializer.data})

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_task_status(request, pk):
    task = Task.objects.get(id=pk, assignee=request.user)
    new_status = request.data.get('status')
    task.status = new_status
    task.save()
    return Response({"message": "Task status updated"})

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'is_admin': user.is_staff  
        })
    return Response({'error': 'Invalid Credentials'}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_dashboard_data(request):
    if not request.user.is_staff:
        return Response({'detail': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

    tasks = Task.objects.all()
    serialized_tasks = TaskSerializer(tasks, many=True)
    users = User.objects.all()
    serialized_users = UserSerializer(users, many=True)

    return Response({
        'tasks': serialized_tasks.data,
        'users': serialized_users.data,
        'admin': request.user.username
    })
