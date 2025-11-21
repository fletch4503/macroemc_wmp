from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Staff(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["last_name", "first_name"]


class Workplaces(models.Model):
    TYPE_CHOICES = [
        ("desktop", "Desktop"),
        ("laptop", "Laptop"),
        ("server", "Server"),
        ("network", "Network Device"),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    ip = models.CharField(max_length=15, blank=True)
    mac = models.CharField(max_length=17, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
