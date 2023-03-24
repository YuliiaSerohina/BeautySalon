from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Services(models.Model):
    name = models.CharField(max_length=100)
    time = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return f'{self.name}, {self.time}, {self.price}'


class Specialist(models.Model):
    LEVEL_SPECIALIST = [(1, 'junior'), (2, 'middle'), (3, 'top')]
    name = models.CharField(max_length=100)
    services = models.ManyToManyField(Services)
    level = models.IntegerField(choices=LEVEL_SPECIALIST)
    phone = PhoneNumberField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}, {self.level}, {self.services}, {self.phone}'


class ScheduleSpecialist(models.Model):
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    date = models.DateField()
    time_start = models.TimeField()
    time_finish = models.TimeField()

    def __str__(self):
        return f'{self.specialist}, {self.date}, {self.time_start}, {self.time_finish}'


class Booking(models.Model):
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    client = models.IntegerField()
    date = models.DateField()
    time_start = models.TimeField()
    status = models.BooleanField(default=True)

















