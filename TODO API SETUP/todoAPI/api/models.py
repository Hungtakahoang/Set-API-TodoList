from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class TodoLists(models.Model):
    todoID = models.AutoField(primary_key=True)
    todoName = models.CharField(max_length=100, null=False, blank=False)
    UserID = models.IntegerField(null=False, blank=False)
    UserName = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    todoDescription = models.TextField()
    todoStatus = models.BooleanField(default=False)
    DateCompleted = models.DateField()
    DateCreated = models.DateTimeField(auto_now_add=True)
    DateUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"TODO: {self.todoID} - {self.todoName}"

    class Meta:
        order_with_respect_to = 'UserName'
