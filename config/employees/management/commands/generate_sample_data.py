from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from employees.models import Department, Employee, Attendance, PerformanceReview
from faker import Faker
import random
from datetime import datetime, timedelta
from decimal import Decimal

fake = Faker()

class Command(BaseCommand):
    help = 'Generate sample employee data'

    def handle(self, *args, **options):
        self.stdout.write('Generating sample data...')
        
        # Create superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write('Created superuser: admin/admin123')
        
        # Create departments
        departments_data = [
            {'name': 'Engineering', 'location': 'Floor 3', 'budget': 500000},
            {'name': 'Marketing', 'location': 'Floor 2', 'budget': 300000},
            {'name': 'Sales', 'location': 'Floor 1', 'budget': 400000},
            {'name': 'HR', 'location': 'Floor 2', 'budget': 200000},
            {'name': 'Finance', 'location': 'Floor 4', 'budget': 350000},
        ]
        
        departments = []
        for dept_data in departments_data:
            dept, created = Department.objects.get_or_create(
                name=dept_data['name'],
                defaults={
                    'description': f"{dept_data['name']} Department",
                    'location': dept_data['location'],
                    'budget': dept_data['budget'],
                    'established_date': fake.date_between(start_date='-5y', end_date='-1y'),
                    'head_of_department': fake.name(),
                    'email': f"{dept_data['name'].lower()}@company.com"
                }
            )
            departments.append(dept)
        
        # Create employees
        employment_types = ['FT', 'PT', 'CT', 'IN']
        job_titles = {
            'Engineering': ['Software Engineer', 'Senior Developer', 'Tech Lead', 'QA Engineer'],
            'Marketing': ['Marketing Specialist', 'Content Writer', 'SEO Analyst', 'Social Media Manager'],
            'Sales': ['Sales Representative', 'Account Manager', 'Sales Director', 'Business Development'],
            'HR': ['HR Manager', 'Recruiter', 'Training Specialist', 'Compensation Analyst'],
            'Finance': ['Accountant', 'Financial Analyst', 'Finance Manager', 'Auditor']
        }
        
        employees = []
        for i in range(20):  # Create 20 employees
            dept = random.choice(departments)
            job_title = random.choice(job_titles[dept.name])
            
            emp = Employee.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                phone=fake.phone_number()[:15],
                hire_date=fake.date_between(start_date='-3y', end_date='today'),
                job_title=job_title,
                salary=Decimal(random.randrange(40000, 120000, 5000)),
                department=dept,
                employment_type=random.choice(employment_types),
                date_of_birth=fake.date_of_birth(minimum_age=22, maximum_age=65),
                address=fake.address()
            )
            employees.append(emp)
        
        # Set managers for some employees
        for emp in employees[5:]:  # Skip first 5 to be managers
            emp.manager = random.choice(employees[:5])
            emp.save()
        
        # Create attendance records
        status_choices = ['PR', 'AB', 'LV', 'HD', 'LT']
        for emp in employees:
            for day in range(30):  # Last 30 days
                date = datetime.now().date() - timedelta(days=day)
                
                # Skip weekends occasionally
                if date.weekday() >= 5 and random.random() > 0.2:
                    continue
                
                status = random.choices(
                    status_choices,
                    weights=[70, 5, 10, 5, 10]  # Weighted probabilities
                )[0]
                
                check_in = None
                check_out = None
                hours_worked = None
                
                if status == 'PR':  # Present
                    check_in = fake.time_object()
                    check_out = (datetime.combine(date, check_in) + timedelta(hours=8)).time()
                    hours_worked = 8.0
                elif status == 'LT':  # Late
                    check_in = (datetime.combine(date, datetime.min.time()) + timedelta(hours=10)).time()
                    check_out = (datetime.combine(date, check_in) + timedelta(hours=7)).time()
                    hours_worked = 7.0
                elif status == 'HD':  # Half day
                    check_in = fake.time_object()
                    check_out = (datetime.combine(date, check_in) + timedelta(hours=4)).time()
                    hours_worked = 4.0
                
                Attendance.objects.create(
                    employee=emp,
                    date=date,
                    check_in=check_in,
                    check_out=check_out,
                    hours_worked=hours_worked,
                    status=status,
                    notes=fake.sentence() if status in ['AB', 'LV'] else '',
                    overtime_hours=Decimal(random.randrange(0, 5)) if status == 'PR' and random.random() > 0.7 else 0
                )
        
        # Create performance reviews
        for emp in employees:
            for i in range(2):  # 2 reviews per employee
                review_date = fake.date_between(
                    start_date=emp.hire_date,
                    end_date='today'
                )
                
                PerformanceReview.objects.create(
                    employee=emp,
                    review_date=review_date,
                    reviewer=random.choice(employees[:5]).get_full_name(),
                    rating=random.randint(3, 5),
                    comments=fake.paragraph(),
                    goals=fake.paragraph(),
                    strengths=fake.paragraph(),
                    areas_for_improvement=fake.paragraph(),
                    next_review_date=review_date + timedelta(days=180)
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully generated sample data: '
                f'{Department.objects.count()} departments, '
                f'{Employee.objects.count()} employees, '
                f'{Attendance.objects.count()} attendance records, '
                f'{PerformanceReview.objects.count()} performance reviews'
            )
        )