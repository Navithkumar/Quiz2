from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views

router = DefaultRouter()
router.register(r'departments', views.DepartmentViewSet)
router.register(r'employees', views.EmployeeViewSet)
router.register(r'attendance', views.AttendanceViewSet)
router.register(r'performance-reviews', views.PerformanceReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
    path('departments/analytics/', views.department_analytics, name='department-analytics'),
    path('attendance/analytics/', views.attendance_analytics, name='attendance-analytics'),
    path('dashboard/', views.employee_dashboard, name='employee-dashboard'),
    path('dashboard/view/', views.dashboard_view, name='dashboard-view'),
]