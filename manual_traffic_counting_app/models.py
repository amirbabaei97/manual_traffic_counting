from django.db import models
from django.utils import timezone

class CarType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='car_types/', null=True, blank=True)
    def __str__(self):
        return self.name
class CountingSession(models.Model):
    STREAM_CHOICES = [(i, str(i)) for i in range(1, 13)]  
    
    name = models.CharField(max_length=100)
    direction = models.CharField(max_length=100)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    streams = models.CharField(max_length=100, blank=True)
    car_types = models.ManyToManyField(CarType, blank=True)  

    def __str__(self):
        return f"{self.name} - {self.start_time}"
class CarCount(models.Model):
    car_type = models.ForeignKey(CarType, on_delete=models.CASCADE)
    session = models.ForeignKey(CountingSession, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    stream_number = models.IntegerField(null=True, blank=True)  

    def __str__(self):
        return f"{self.car_type} - {self.timestamp}"

