from django.db import models

# Create your models here.
class department(models.Model):
    department_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,unique=True)

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(department, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10,decimal_places=2)
    join_date = models.DateField()
