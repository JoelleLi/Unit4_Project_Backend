from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.

class Photo(models.Model):
    url = models.CharField(max_length=200)

    def __str__(self):
        return f"Photo {self.id} @ {self.url}"

class Person(models.Model):
    ALCOHOL_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Sometimes', 'Sometimes'),
    ]

    SURPRISES_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Sometimes', 'Sometimes'),
    ]

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    image = models.ForeignKey(Photo, null=True, blank=True, on_delete=models.SET_NULL)
    birthday = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    card = models.BooleanField(default=False)
    present = models.BooleanField(default=False)
    colours = models.CharField(max_length=100, null=True, blank=True)
    cake = models.CharField(max_length=100, null=True, blank=True)
    dietary = models.CharField(max_length=100, null=True, blank=True)
    flowers = models.CharField(max_length=100, null=True, blank=True)
    brands = models.CharField(max_length=300, null=True, blank=True)
    likes_surprises = models.CharField(max_length=10, choices=SURPRISES_CHOICES, blank=True, null=True, default=None)
    drinks_alcohol = models.CharField(max_length=10, choices=ALCOHOL_CHOICES, blank=True, null=True, default=None)

    def __str__(self):
        return f'Created by: {self.created_by.first_name}, Person: {self.first_name}, ID: ({self.id})'
    
    def delete(self, *args, **kwargs):
        if self.image:  # Check if there is an associated Photo object
            self.image.delete()  # Delete the Photo object
        super().delete(*args, **kwargs)  # Call the superclass method to delete the Person object

class Wish(models.Model):
    PRIORITY_CHOICES = [
        ('High', 'Desparately Want'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    name = models.CharField(max_length=100)
    images = models.ManyToManyField(Photo, blank=True)    
    url = models.CharField(max_length=800, blank=True)
    description = models.CharField(max_length=500, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    reserved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f'Name: {self.name}, ID: ({self.id})'
    
    def delete(self, *args, **kwargs):
        # Iterate over the related Photo objects and delete them
        for photo in self.images.all():
            photo.delete()
        super().delete(*args, **kwargs)# Call the superclass method to delete the Person object

class UserProfile(models.Model):
    ALCOHOL_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Sometimes', 'Sometimes'),
    ]

    SURPRISES_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Sometimes', 'Sometimes'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    image = models.ForeignKey(Photo, null=True, blank=True, on_delete=models.SET_NULL)
    colours = models.CharField(max_length=100, blank=True)
    cake = models.CharField(max_length=100, blank=True)
    dietary = models.CharField(max_length=100, blank=True)
    flowers = models.CharField(max_length=100, blank=True)
    brands = models.CharField(max_length=300, blank=True)
    likes_surprises = models.CharField(max_length=10, choices=SURPRISES_CHOICES, blank=True, null=True, default=None)
    drinks_alcohol = models.CharField(max_length=10, choices=ALCOHOL_CHOICES, blank=True, null=True, default=None)
    
    def __str__(self):
        return f'Primary User ID: {self.user.id}, Name: {self.user.first_name}, Profile ID: ({self.id})'
    
# class Thing(models.Model):
#     name = models.CharField(max_length=80, null=True, blank=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
#     person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)

#     def __str__(self):
#         return f'Thing: {self.name}, ID: ({self.id})'
    
# class Note(models.Model):
#     date = models.DateTimeField
#     name = models.CharField(max_length=80)
#     entry = models.CharField(max_length=500)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
#     person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)

#     def __str__(self):
#         return f'Note made: {self.name}, ID: ({self.id})' 