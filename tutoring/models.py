
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class Student(models.Model):
    tutor = models.ForeignKey(Tutor, related_name='students', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class Session(models.Model):
    tutor = models.ForeignKey(Tutor, related_name='sessions', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='sessions', on_delete=models.CASCADE)
    date = models.DateField()
    duration = models.IntegerField(help_text="Duration in minutes")
    topic = models.CharField(max_length=200)

    def __str__(self):
        return f"Session on {self.topic} with {self.student.name}"
