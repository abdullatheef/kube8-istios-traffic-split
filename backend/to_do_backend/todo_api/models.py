from django.db import models

# Create your models here.


from django.contrib.auth.models import User

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to User model for userid
    item = models.CharField(max_length=255)  # Field for the item description

    def __str__(self):
        return f'{self.user.username} - {self.item}'
    


    

