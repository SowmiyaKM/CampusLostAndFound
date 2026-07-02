from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CampusUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'student_id', 'department', 'year', 'phone', 'is_staff', 'created_at')
    list_filter = ('department', 'year', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'student_id', 'first_name', 'last_name')
    fieldsets = UserAdmin.fieldsets + (
        ('Campus Info', {'fields': ('student_id', 'department', 'year', 'phone', 'avatar')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Campus Info', {'fields': ('email', 'student_id', 'department', 'year', 'phone')}),
    )
