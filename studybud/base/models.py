# Accounts:
#   justin
#   Justin_Bui13

#   random_man
#   Random_Password13


from django.db import models
from django.contrib.auth.models import User # Yes, Django does have a built in User class in the admin panel


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# Create your models here.
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # Whenever we SET_NULL on delete, we must specify that it can be null in the database
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)

    # null=True means that there can be blank values on the database
    # blank=True also allows empty sections when submitting forms
    description = models.TextField(null=True, blank=True)
    
    participants = models.ManyToManyField(User, related_name='participants', blank=True) # Since we already have a user as as foreign key, we will specify related_name to 'participants'
    
    updated = models.DateTimeField(auto_now=True) # auto_now takes a snapshot for everytime we save an item
    created = models.DateTimeField(auto_now_add=True) # auto_now_add only takes a timestamp when we FIRST create/save this instance

    # Allows all of the rooms to be displayed in order
    class Meta:
        ordering = ['-updated', '-created'] # Order in descending order ('updated' means ASCENDING)

    def __str__(self):
        return self.name


class Message(models.Model):
    # One to many (1 user with many messages)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Many to one relationship (Or one to many) - Where Room is the parent containing multiple children (messages)
    room = models.ForeignKey(Room, # Room is the parent
                            on_delete=models.CASCADE, # When parent is deleted, all children will be deleted (cascaded)
                            )
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True) # auto_now takes a snapshot for everytime we save an item
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50] # Getting first 50 characters
