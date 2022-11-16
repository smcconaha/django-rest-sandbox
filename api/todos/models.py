from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True) #this is a FK, created during model viewset ex
    #'Category' comes below so can reference it this way
    # on_delete, cascade says when ref object is deleted it will also delete all associated info
    # protect forbids the deletion of the reference object, to delete the ref object you need to get ride of all ref objects

#----MODEL VIEWSET------#
class Category(models.Model):
    name = models.CharField(max_length=60)