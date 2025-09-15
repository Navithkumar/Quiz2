from django.contrib import admin
from .models import Department, Employee, Attendance, PerformanceReview

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'head_of_department', 'budget']
    list_filter = ['location']
    search_fields = ['name', 'head_of_department']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'department', 'job_title', 'salary']
    list_filter = ['department', 'employment_type']
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ['date_of_birth']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'status', 'hours_worked', 'check_in', 'check_out']
    list_filter = ['status', 'date']
    search_fields = ['employee__first_name', 'employee__last_name']
    date_hierarchy = 'date'

@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ['employee', 'review_date', 'rating', 'reviewer']
    list_filter = ['rating', 'review_date']
    search_fields = ['employee__first_name', 'employee__last_name', 'reviewer']
    date_hierarchy = 'review_date'