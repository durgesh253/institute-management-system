from django.urls import path
from . import views
urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('logout/', views.logout, name='logout'),
    path('profile_update/<str:employee_id>',views.update_profile, name="profile_update"),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('otp_verification/', views.otp_verification, name='otp_verification'),
    path('resend_otp/', views.resend_otp, name="resend_otp"),
    path('dashboard_view/', views.dashboard_view, name='dashboard_view'),
    path('student_register_view/', views.student_register_view, name="student_register_view"),
    path('students_view/', views.students_view, name='students_view'),
    path('staff_view/', views.staff_view, name='staff_view'),
    path('batches/', views.batches, name='batches'),
    path('create_batch/',views.create_batch, name="create_batch"),
    path("update_batch/<int:batch_id>", views.update_batch, name='update_batch'),
    path('my_request/', views.my_request, name='my_request'),
    path('delete_request/<int:leave_id>', views.delete_request, name='delete_request'),
    path("delete_student/<int:student_id>", views.delete_student, name='delete_student'),
    path("update_student/<int:student_id>", views.update_student, name='update_student'),
    path('profile_view/', views.profile_view, name='profile_view'),
    path('create_post/',views.create_post,name='create_post'),
    path('social_list/',views.social_list, name="social_list"),
    path('post_delete/<int:post_id>',views.delete_post,name='post_delete'),
    path('edit_post/<int:post_id>',views.edit_post,name='edit_post'),
   
]