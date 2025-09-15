from rest_framework import serializers
from .models import Department, Employee, Attendance, PerformanceReview

class DepartmentSerializer(serializers.ModelSerializer):
    employee_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = '__all__'
    
    def get_employee_count(self, obj):
        return obj.employees.count()

class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    manager_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Employee
        fields = '__all__'
    
    def get_manager_name(self, obj):
        return f"{obj.manager.first_name} {obj.manager.last_name}" if obj.manager else None

class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.__str__', read_only=True)
    
    class Meta:
        model = Attendance
        fields = '__all__'

class PerformanceReviewSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.__str__', read_only=True)
    
    class Meta:
        model = PerformanceReview
        fields = '__all__'

class DepartmentAnalyticsSerializer(serializers.Serializer):
    department = serializers.CharField()
    employee_count = serializers.IntegerField()
    avg_salary = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_budget = serializers.DecimalField(max_digits=12, decimal_places=2)
    budget_utilization = serializers.DecimalField(max_digits=5, decimal_places=2)

class AttendanceAnalyticsSerializer(serializers.Serializer):
    date = serializers.DateField()
    present_count = serializers.IntegerField()
    absent_count = serializers.IntegerField()
    late_count = serializers.IntegerField()
    attendance_rate = serializers.DecimalField(max_digits=5, decimal_places=2)