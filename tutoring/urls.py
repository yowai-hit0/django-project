from django.urls import path
from .views import dashboard, add_student, edit_student, delete_student, add_session, edit_session, delete_session, home, register
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', home, name='home'),  
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='tutoring/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('student/add/',add_student, name='add_student'),
    path('student/edit/<int:student_id>/', edit_student, name='edit_student'),
    path('student/delete/<int:student_id>/', delete_student, name='delete_student'),
     path('session/add/', add_session, name='add_session'),
    path('session/edit/<int:session_id>/', edit_session, name='edit_session'),
    path('session/delete/<int:session_id>/', delete_session, name='delete_session'),
]
