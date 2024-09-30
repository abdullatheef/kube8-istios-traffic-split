# todo/views.py

from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegisterSerializer, UserLoginSerializer
from .tasks import delete_todo_task
import logging
logger = logging.getLogger(__name__)
import os

# todo/views.py

class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)



class TodoListCreateView(APIView):
    def get(self, request, *args, **kwargs):
        """List all todos for the authenticated user with pagination."""
        todos = Todo.objects.filter(user=request.user)
        print(">>>>>")        
        logger.info("mmmmmm")
        print(os.environ.get('APP_VERSION_CUSTOM'))
        logger.info(os.environ.get('APP_VERSION_CUSTOM'))
        # Instantiate a paginator and paginate the queryset
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Customize the page size
        result_page = paginator.paginate_queryset(todos, request)
        
        serializer = TodoSerializer(result_page, many=True)
        #return Response({"version": os.environ.get('APP_VERSION_CUSTOM')})
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        """Add a new todo item."""
        data = request.data.copy()
        data['user'] = request.user.id  # Explicitly set the user from the authenticated request
        
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TodoDeleteView(APIView):
    # def delete(self, request, todo_id, *args, **kwargs):
    #     """Delete a specific todo item."""
    #     todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    #     todo.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    
    def delete(self, request, todo_id, *args, **kwargs):
        delete_todo_task.delay(todo_id)  # Call the Celery task
        return Response({'message': 'Todo deletion has been scheduled.'}, status=status.HTTP_202_ACCEPTED)

