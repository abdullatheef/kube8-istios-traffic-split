# todo/urls.py

from django.urls import path
from .views import TodoListCreateView, TodoDeleteView

urlpatterns = [
    path('todos/', TodoListCreateView.as_view(), name='todo-list-create'),  # GET for list, POST for add
    path('todos/<int:todo_id>/', TodoDeleteView.as_view(), name='todo-delete'),  # DELETE for deleting a todo
]


