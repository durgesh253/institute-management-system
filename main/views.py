from django.shortcuts import render, redirect
from .models import employee, StudentRegistration,LeaveRequest,LeaveType,Batch
from django.contrib import messages
from django.conf import settings
import random
from django.core.mail import send_mail

def login_view(request):
    if request.method == 'POST':
        employee_id = request.POST['Employee_id']
        password = request.POST['password']
        # print(employee_id, password)
        try:
            CHECK_EMPLOYEE = employee.objects.get(employee_id=employee_id)
        except employee.DoesNotExist:
            print("Invalid credential")
        except Exception as e:
            print(f"ERROR : {e}")
        else:
            if CHECK_EMPLOYEE.employee_id == employee_id and CHECK_EMPLOYEE.password == password:
                request.session['employee_id'] = employee_id
                employe_data = employee.objects.get(employee_id=employee_id)
                request.session['role'] = employe_data.role.name
                request.session['first_name'] = employe_data.first_name
                request.session['last_name'] = employe_data.last_name
                request.session['email'] = employe_data.email
                request.session['mobile'] = employe_data.mobile
                print("Now you are logged in")
                return redirect('dashboard_view')
            else:
                print("Email or password doesn't match")
                

    return render(request, 'login.html')

def logout(request):
    del request.session['employee_id']
    messages.success(request,'Now You are logged out')
    return redirect(login_view)

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        # print(email)
        try:
            CHECK_EMPLOYEE = employee.objects.get(email=email)
        except employee.DoesNotExist:
            messages.info(request, 'User Does not exist')
        else:
            otp = random.randint(000000,999999)
            subject = 'otp for forget password'
            message = f"""
            Your otp is : {otp}
             """
            from_email = settings.EMAIL_HOST_USER
            resipent_list = [f"{email}"]
            send_mail(subject, message, from_email, resipent_list)
            CHECK_EMPLOYEE.otp = otp
            CHECK_EMPLOYEE.save()
            context = {
                'email' : email
            }
            messages.success(request, 'Please, check your mail. OTP sent successfully')
            return render(request ,  'otp-verification.html' , context)
            
    return render(request, 'forgot-password.html',)

def otp_verification(request):
    if request.method == 'POST':
        email = request.POST['email']
        otp = request.POST['otp']
        new_password = request.POST['new_password']
        confirm_password =  request.POST['confirm_password']
        try:
            CHECK_EMPLOYEE = employee.objects.get(email=email)
            context = {
                'email' : email
            }
        except employee.DoesNotExist:
            messages.info(request, 'User does not exist')
            return redirect('login_view')
        else:
            if CHECK_EMPLOYEE.otp == otp:
                if new_password == confirm_password:
                   CHECK_EMPLOYEE.password == new_password
                   CHECK_EMPLOYEE.save()
                   messages.success(request, "Password changed Succesfully")
                   return redirect('login_view')
                else:
                    messages.error(request,'New password and confirm Password does not match')
                    return render(request,'otp-verification.html', context)
            else:
                messages.error(request,"OTP invalid!")
                return render(request,'otp-verification.html', context)
    return render(request, 'login.html')


def resend_otp(request):
    if request.method == 'POST':
        email = request.POST['email']

        try:
            CHECK_EMPLOYEE = employee.objects.get(email=email)
        except employee.DoesNotExist:
            messages.error(request, 'User does not exist')
            return redirect('login_view')
        else:
            otp = random.randint(000000,999999)
            subject = "Resend Otp Is"
            message = f"""
                  Your otp is = {otp}
                  """
            from_email = settings.EMAIL_HOST_USER
            resipent_list = [f"{email}"]
            send_mail(subject, message, from_email, resipent_list)
            CHECK_EMPLOYEE.otp = otp
            CHECK_EMPLOYEE.save()
            messages.success(request, "Otp sent successfully. Check Your Gmail")
            return render(request ,  'otp-verification.html')
    return render(request,'resend_otp.html')



        
def dashboard_view(request):
    total_students = StudentRegistration.objects.count()
    total_employee = employee.objects.count() 
    total_batches = Batch.objects.count()
    total_request = LeaveRequest.objects.count()
    faculties_leaves = LeaveRequest.objects.all()
    
    
    context = {
        'total_students' : total_students,
        'total_employee' : total_employee,
        'total_batches' : total_batches,
        'total_request' : total_request,
        'faculties_leaves':faculties_leaves,
         
    }
    return render(request, 'dashboard.html',context)

def student_register_view(request):
    if request.method == "POST":
        profile = request.FILES['profile']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        mobile = request.POST['mobile']
        gender = request.POST['gender']
        date_of_birth = request.POST['dob']
        course = request.POST['course']

        new_student = StudentRegistration.objects.create(
            profile = profile,
            first_name = firstname,
            last_name = lastname,
            email = email,
            mobile = mobile,
            gender = gender,
            dob = date_of_birth,
            course = course,
        )
        new_student.save()
        return redirect('dashboard_view')


def students_view(request):
    students = StudentRegistration.objects.all()

    context = {
      'students':students
    }
    return render(request, 'students.html', context)

def staff_view(request):
    employee_ = employee.objects.all()
    context = {
        'employess' : employee_
    }
    
    return render(request, 'staffs-view.html' , context)

def update_student(request, student_id):
    if request.method == 'POST':
        profile = request.FILES['profile']
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        email = request.POST['email']
        mobile = request.POST['mobile']
        dob = request.POST['dob']

        getStudent = StudentRegistration.objects.get(id=student_id)
        getStudent.profile = profile
        getStudent.first_name = fname
        getStudent.last_name = lname
        getStudent.email = email
        getStudent.mobile = mobile
        getStudent.dob = dob
        getStudent.save()
        return redirect('students_view')

    # This part should not be indented as it should be at the same level as the if statement
    getStudent = StudentRegistration.objects.get(id=student_id)
    context = {
        'profile': getStudent.profile,
        'fname': getStudent.first_name,
        'lname': getStudent.last_name,
        'email': getStudent.email,
        'mobile': getStudent.mobile,
        'dob': getStudent.dob.strftime('%Y-%m-%d'),
        'course': getStudent.course
    }
    return render(request, 'student_edit.html', context)

def delete_student(request, student_id):
    getStudent = StudentRegistration.objects.get(id=student_id)
    getStudent.delete()
    return redirect('students_view')



def my_request(request):
    get_emplpoyee = employee.objects.get(employee_id=request.session['employee_id'])

    if request.method == 'POST':
        leave_type =  request.POST['leave_type']
        duration = request.POST['duration']
        from_date = request.POST['from_date']
        to_date =  request.POST['to_date']
        reason = request.POST['reason']
        employee_id = get_emplpoyee.id
        new_leave_request = LeaveRequest.objects.create(    
            employee_id_id = employee_id,
            leave_type_id = leave_type,
            duration = duration,
            from_date = from_date,
            to_date = to_date,
            reason = reason
        )
        new_leave_request.save()
        return redirect('my_request')
    leaves = LeaveType.objects.all()
    leave_requests = LeaveRequest.objects.filter(employee_id_id =get_emplpoyee.id)
         
    context = {
        'leaves' : leaves,
        'leave_requests' : leave_requests,
    }

    return render(request, 'my-request.html', context)

def batches(request):
      batches = Batch.objects.all()
      faculty_list = employee.objects.all()
      student_list = StudentRegistration.objects.all()
      return render(request, 'batches.html',{'batches': batches,'faculty_list': faculty_list, 'student_list': student_list})


def create_batch(request):
    # Display the form for GET request
    if request.method == 'GET':
        faculty_list = employee.objects.all()
        student_list = StudentRegistration.objects.all()
        return render(request, 'create_batch.html', {'faculty_list': faculty_list, 'student_list': student_list})

    # Process the form for POST request
    elif request.method == 'POST':
        batch_name = request.POST['batch_name']
        faculty_id = request.POST['faculty']
        students_ids = request.POST.getlist('students')  # Use getlist to get multiple values
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']

        try:
            faculty = employee.objects.get(id=faculty_id)
        except employee.DoesNotExist:
            return render(request, 'error.html', {'error_message': 'Invalid faculty ID'})

        students = StudentRegistration.objects.filter(id__in=students_ids)

        new_batch = Batch.objects.create(
            batch_name=batch_name,
            faculty=faculty,
            start_time=start_time,
            end_time=end_time
        )

        # Use set() method to handle many-to-many relationship
        new_batch.students.set(students)

        return redirect('batches')

def delete_request(request, leave_id):
    get_leave = LeaveRequest.objects.get(id=leave_id)
    get_leave.delete()
    return redirect('my_request')


def profile_view(request):
    return render(request, 'profile.html')