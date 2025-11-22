from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    archived = models.BooleanField(default=False)

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
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["last_name", "first_name"]


class Workplaces(models.Model):
    TYPE_CHOICES = [
        ("nopcplace", "Место без компьютера"),
        ("pcplace", "Место с компьютером"),
    ]
    name = models.CharField(max_length=100, verbose_name="Название Рабочего Места:")
    description = models.TextField(verbose_name="Описание Рабочего Места:")
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, verbose_name="Тип Рабочего Места:")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Тип Рабочего Места:")
    ip = models.CharField(max_length=15, blank=True)
    mac = models.CharField(max_length=17, blank=True)
    archived = models.BooleanField(default=False)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]
