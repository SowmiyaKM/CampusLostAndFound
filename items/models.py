from django.conf import settings
from django.db import models
from django.urls import reverse

CATEGORY_CHOICES = [
    ('electronics', 'Electronics'),
    ('id_cards', 'ID Cards'),
    ('books', 'Books'),
    ('wallets', 'Wallets'),
    ('keys', 'Keys'),
    ('accessories', 'Accessories'),
    ('clothing', 'Clothing'),
    ('others', 'Others'),
]


class LostItem(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('found', 'Found'),
    ]

    title = models.CharField(max_length=150)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    image = models.ImageField(upload_to='lost_items/', blank=True, null=True)
    location = models.CharField(max_length=150, help_text="Last seen location")
    date_lost = models.DateField()
    reward = models.CharField(max_length=100, blank=True, help_text="Optional reward")
    contact_info = models.CharField(max_length=150, help_text="Phone or email to contact")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lost_items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[Lost] {self.title}"

    def get_absolute_url(self):
        return reverse('items:lost_detail', args=[self.pk])

    @property
    def kind(self):
        return 'lost'


class FoundItem(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('returned', 'Returned'),
    ]

    title = models.CharField(max_length=150)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    image = models.ImageField(upload_to='found_items/', blank=True, null=True)
    location = models.CharField(max_length=150, help_text="Found location")
    date_found = models.DateField()
    contact_info = models.CharField(max_length=150, help_text="Phone or email to contact")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    finder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='found_items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[Found] {self.title}"

    def get_absolute_url(self):
        return reverse('items:found_detail', args=[self.pk])

    @property
    def kind(self):
        return 'found'


class Notification(models.Model):
    TYPE_CHOICES = [
        ('match', 'Potential Match'),
        ('returned', 'Item Returned'),
        ('announcement', 'Admin Announcement'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    notif_type = models.CharField(max_length=15, choices=TYPE_CHOICES, default='announcement')
    link = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.message[:40]}"
