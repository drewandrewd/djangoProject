from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=[('leader', 'Руководитель'), ('specialist', 'Специалист'),
                                                        ('clerk', 'Служащий'), ('worker', 'Рабочий')])

    class Meta:
        app_label = 'djangoProject'


class Employee(models.Model):
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    class Meta:
        app_label = 'djangoProject'
