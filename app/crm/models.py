from django.db import models
from django.contrib.auth.models import AbstractUser


class ManagerUser(AbstractUser):
    email = models.EmailField(unique=True)
    patronymic = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=15)


    def __str__(self):
        return self.email





class Apartment(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активно'),
        ('reserved', 'Бронь'),
        ('sold', 'Куплено'),
        ('installments', 'Рассрочка'),
        ('barter', 'Бартер'),
    ]

    address = models.CharField(max_length=255)
    floor = models.IntegerField()
    area = models.FloatField()
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.address} - {self.status}"

class Client(models.Model):
    full_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    contract_number = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=Apartment.STATUS_CHOICES)
    apartment = models.ForeignKey(Apartment, related_name='clients', on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name
