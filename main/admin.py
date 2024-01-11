from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail

from .models import role, employee, StudentRegistration, LeaveRequest,LeaveType,Batch,Socials
# Register your models here.

admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(role)

class employeeAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        subject = 'Employee login credential at "IMS"'
        from_mail = 'brijeshgondaliya.tops@gmail.com'
        recipient_list = [f'{obj.email}']

        context = {
            'first_name': obj.first_name,
            'last_name': obj.last_name,
            'employee_email': obj.email,
            'employee_password': obj.password
        }

        print(context)

        html_message = render_to_string('mail-templates\login-credential-mail.html', context)
        plain_message = strip_tags(html_message)

        send_mail(
            subject, plain_message, from_mail, recipient_list,
            html_message=html_message,
        )
admin.site.register(employee, employeeAdmin)
admin.site.register(StudentRegistration)
admin.site.register(LeaveRequest)
admin.site.register(LeaveType)
admin.site.register(Batch)
admin.site.register(Socials)