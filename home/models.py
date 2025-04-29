from django.db import models


class Color(models.Model):
    color_name = models.CharField(max_length=200)

class Person(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    color = models.ForeignKey(Color, null=True, blank=True, on_delete=models.CASCADE)
