from django.db import models
from django.utils import timezone
from main.utils import file_helpers
import string
import random

# Create your models here.
# class 

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class role(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(role, self).save(*args, **kwargs)

class employee(BaseModel):
    profile = models.ImageField(upload_to=file_helpers.custom_file_name, default='default-images\Ellipse_2.png')
    employee_id = models.CharField(max_length=10, unique=True, editable=False)
    role = models.ForeignKey(role, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True, blank=False)
    mobile = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    otp = models.CharField(max_length=20, default='123456')


    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.employee_id:
            # Generate the custom ID if it doesn't exist
            last_id = employee.objects.all().order_by('-id').first()
            if last_id:
                last_id = last_id.employee_id
                last_id = last_id.replace('IM', '')
                last_id = int(last_id)
                new_id = f'IM{str(last_id + 1).zfill(4)}'
            else:
                new_id = 'IM0001'
            self.employee_id = new_id

        if not self.password:
            # Generate a random password
            password_characters = string.ascii_letters + string.digits + '@#_!'
            random_password = ''.join(random.choice(password_characters) for i in range(8))
            self.password = random_password.upper()

        super(employee, self).save(*args, **kwargs)

class courses(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class StudentRegistration(BaseModel):
    profile = models.ImageField(upload_to='students/')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email= models.EmailField(max_length=100)
    mobile = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    dob = models.DateField()
    course = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id} - {self.first_name} {self.last_name}"
    
class LeaveType(BaseModel):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class LeaveRequest(BaseModel):
    employee_id = models.ForeignKey(employee, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    duration  = models.CharField(max_length=50)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()

class Batch(models.Model):
    batch_id = models.AutoField(primary_key=True)
    batch_name = models.CharField(max_length=255)
    faculty = models.ForeignKey(employee, on_delete=models.CASCADE)
    students = models.ManyToManyField(StudentRegistration)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    
    def __str__(self):
        return self.batch_name

    
