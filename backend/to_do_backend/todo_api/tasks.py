# todos/tasks.py
from to_do_backend.celery import app
from .models import Todo

@app.task
def delete_todo_task(todo_id):
    try:
        todo = Todo.objects.get(id=todo_id)
        todo.delete()
        return f'Todo with ID {todo_id} has been deleted.'
    except Todo.DoesNotExist:
        return f'Todo with ID {todo_id} does not exist.'
