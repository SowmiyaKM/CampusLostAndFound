from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    DEPARTMENT_CHOICES = [
        ('CSE', 'Computer Science & Engineering'),
        ('ECE', 'Electronics & Communication Engineering'),
        ('EEE', 'Electrical & Electronics Engineering'),
        ('MECH', 'Mechanical Engineering'),
        ('CIVIL', 'Civil Engineering'),
        ('IT', 'Information Technology'),
        ('AIDS', 'AI & Data Science'),
        ('OTHER', 'Other'),
    ]
    YEAR_CHOICES = [
        (1, '1st Year'),
        (2, '2nd Year'),
        (3, '3rd Year'),
        (4, '4th Year'),
    ]

    student_id = models.CharField(max_length=30, unique=True)
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES, default='CSE')
    year = models.IntegerField(choices=YEAR_CHOICES, default=1)
    phone = models.CharField(max_length=15)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.student_id})"
