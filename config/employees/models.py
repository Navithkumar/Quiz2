from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    established_date = models.DateField()
    head_of_department = models.CharField(max_length=100)
    email = models.EmailField()
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Employee(models.Model):
    EMPLOYMENT_TYPES = [
        ('FT', 'Full-Time'),
        ('PT', 'Part-Time'),
        ('CT', 'Contract'),
        ('IN', 'Intern'),
    ]
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    hire_date = models.DateField()
    job_title = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees')
    employment_type = models.CharField(max_length=2, choices=EMPLOYMENT_TYPES, default='FT')
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    date_of_birth = models.DateField()
    address = models.TextField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    class Meta:
        ordering = ['last_name', 'first_name']

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('PR', 'Present'),
        ('AB', 'Absent'),
        ('LV', 'On Leave'),
        ('HD', 'Half Day'),
        ('LT', 'Late'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    hours_worked = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='PR')
    notes = models.TextField(blank=True)
    overtime_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    leave_type = models.CharField(max_length=50, blank=True)
    
    class Meta:
        unique_together = ['employee', 'date']
        ordering = ['-date', 'employee']
    
    def __str__(self):
        return f"{self.employee} - {self.date} ({self.status})"

class PerformanceReview(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='performance_reviews')
    review_date = models.DateField()
    reviewer = models.CharField(max_length=100)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comments = models.TextField()
    goals = models.TextField()
    strengths = models.TextField()
    areas_for_improvement = models.TextField()
    next_review_date = models.DateField()
    
    class Meta:
        ordering = ['-review_date']
    
    def __str__(self):
        return f"{self.employee} - {self.review_date} (Rating: {self.rating})"