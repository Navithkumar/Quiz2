from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
from .models import Department, Employee, Attendance, PerformanceReview
from .serializers import (
    DepartmentSerializer, EmployeeSerializer, AttendanceSerializer, 
    PerformanceReviewSerializer, DepartmentAnalyticsSerializer, AttendanceAnalyticsSerializer
)
from datetime import timedelta
from django.shortcuts import render


def dashboard_view(request):
    return render(request, 'employees/index.html')


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            return Response({
                "is_v1": True,
                "data": response.data
            })
        except Exception as e:
            return Response({
                "is_v1": True,
                "data": {"error": str(e)}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            queryset = Employee.objects.all()
            department = self.request.query_params.get('department')
            employment_type = self.request.query_params.get('employment_type')
            if department:
                queryset = queryset.filter(department__name__icontains=department)
            if employment_type:
                queryset = queryset.filter(employment_type=employment_type)
            return queryset
        except Exception as e:
            print("Error in EmployeeViewSet:", e)
            return Employee.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            return Response({
                "is_v1": True,
                "data": response.data
            })
        except Exception as e:
            return Response({
                "is_v1": True,
                "data": {"error": str(e)}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            queryset = Attendance.objects.all()
            employee = self.request.query_params.get('employee')
            date = self.request.query_params.get('date')
            status_param = self.request.query_params.get('status')
            if employee:
                queryset = queryset.filter(employee__last_name__icontains=employee)
            if date:
                queryset = queryset.filter(date=date)
            if status_param:
                queryset = queryset.filter(status=status_param)
            return queryset
        except Exception as e:
            print("Error in AttendanceViewSet:", e)
            return Attendance.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            return Response({
                "is_v1": True,
                "data": response.data
            })
        except Exception as e:
            return Response({
                "is_v1": True,
                "data": {"error": str(e)}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PerformanceReviewViewSet(viewsets.ModelViewSet):
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            queryset = PerformanceReview.objects.all()
            employee = self.request.query_params.get('employee')
            min_rating = self.request.query_params.get('min_rating')
            if employee:
                queryset = queryset.filter(employee__last_name__icontains=employee)
            if min_rating:
                queryset = queryset.filter(rating__gte=min_rating)
            return queryset
        except Exception as e:
            print("Error in PerformanceReviewViewSet:", e)
            return PerformanceReview.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            return Response({
                "is_v1": True,
                "data": response.data
            })
        except Exception as e:
            return Response({
                "is_v1": True,
                "data": {"error": str(e)}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def department_analytics(request):
    try:
        departments = Department.objects.all()
        data = []
        for dept in departments:
            employees = dept.employees.all()
            avg_salary = employees.aggregate(avg=Avg('salary'))['avg'] or 0
            total_salary = employees.aggregate(total=Sum('salary'))['total'] or 0
            data.append({
                'department': dept.name,
                'employee_count': employees.count(),
                'avg_salary': avg_salary,
                'total_budget': dept.budget,
                'budget_utilization': (total_salary / dept.budget * 100) if dept.budget > 0 else 0
            })
        serializer = DepartmentAnalyticsSerializer(data, many=True)
        return Response({
            "is_v1": True,
            "data": serializer.data
        })
    except Exception as e:
        return Response({
            "is_v1": True,
            "data": {"error": str(e)}
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attendance_analytics(request):
    try:
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)
        attendance_data = Attendance.objects.filter(
            date__range=[start_date, end_date]
        ).values('date').annotate(
            present_count=Count('id', filter=Q(status='PR')),
            absent_count=Count('id', filter=Q(status='AB')),
            late_count=Count('id', filter=Q(status='LT')),
            total_count=Count('id')
        ).order_by('date')
        data = []
        for item in attendance_data:
            total = item['total_count']
            attendance_rate = (item['present_count'] / total * 100) if total > 0 else 0
            data.append({
                'date': item['date'],
                'present_count': item['present_count'],
                'absent_count': item['absent_count'],
                'late_count': item['late_count'],
                'attendance_rate': attendance_rate
            })
        serializer = AttendanceAnalyticsSerializer(data, many=True)
        return Response({
            "is_v1": True,
            "data": serializer.data
        })
    except Exception as e:
        return Response({
            "is_v1": True,
            "data": {"error": str(e)}
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_dashboard(request):
    try:
        total_employees = Employee.objects.count()
        total_departments = Department.objects.count()
        today_attendance = Attendance.objects.filter(
            date=timezone.now().date()
        ).count()
        recent_hires = Employee.objects.order_by('-hire_date')[:5]
        recent_hires_data = EmployeeSerializer(recent_hires, many=True).data
        return Response({
            "is_v1": True,
            "data": {
                'total_employees': total_employees,
                'total_departments': total_departments,
                'today_attendance': today_attendance,
                'recent_hires': recent_hires_data
            }
        })
    except Exception as e:
        return Response({
            "is_v1": True,
            "data": {"error": str(e)}
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
