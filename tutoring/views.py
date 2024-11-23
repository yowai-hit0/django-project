
from typing import Counter
from django.shortcuts import render, redirect, get_object_or_404
from .models import Tutor, Student, Session
from .forms import StudentForm, SessionForm, UserRegistrationForm, TutorProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from datetime import timedelta
from django.utils import timezone


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'tutoring/landing.html')

@login_required
def dashboard(request):
    tutor = Tutor.objects.get(user=request.user)
    students = tutor.students.all()
    sessions = tutor.sessions.all()

    session_count = Counter(session.student.name for session in sessions)
    labels = list(session_count.keys())  
    data = list(session_count.values())  

    last_7_days = timezone.now() - timedelta(days=7)
    recent_sessions = sessions.filter(date__gte=last_7_days)
    line_labels = [(timezone.now() - timedelta(days=i)).date() for i in range(7)]
    line_data = [recent_sessions.filter(date=(timezone.now() - timedelta(days=i)).date()).count() for i in range(7)]

    return render(request, 'tutoring/dashboard.html', {
        'tutor': tutor,
        'students': students,
        'sessions': sessions,
        'labels': labels,  
        'data': data,  
        'line_labels': line_labels,  
        'line_data': line_data,  
    })

# @login_required
# def dashboard(request):
#     tutor = Tutor.objects.get(user=request.user)  # Get the tutor associated with the logged-in user
#     students = tutor.students.all() 
#     sessions = tutor.sessions.all() 
#     return render(request, 'tutoring/dashboard.html', {
#         'tutor': tutor, 
#         'students': students,
#         'sessions': sessions
#     })


@login_required
def add_student(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        student = form.save(commit=False)
        student.tutor = Tutor.objects.get(user=request.user)
        student.save()
        return redirect('dashboard')
    return render(request, 'tutoring/student_form.html', {'form': form})


@login_required
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id, tutor__user=request.user)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'tutoring/student_form.html', {'form': form})


@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id, tutor__user=request.user)
    student.delete()
    return redirect('dashboard')


@login_required
def add_session(request):
    tutor = Tutor.objects.get(user=request.user)
    form = SessionForm(request.POST or None)
    form.fields['student'].queryset = tutor.students.all()  # Restrict to tutor's students
    if form.is_valid():
        session = form.save(commit=False)
        session.tutor = tutor
        session.save()
        return redirect('dashboard')
    return render(request, 'tutoring/session_form.html', {'form': form})

@login_required
def edit_session(request, session_id):
    session = get_object_or_404(Session, id=session_id, tutor__user=request.user)
    form = SessionForm(request.POST or None, instance=session)
    form.fields['student'].queryset = session.tutor.students.all()  # Restrict to tutor's students
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'tutoring/session_form.html', {'form': form})

@login_required
def delete_session(request, session_id):
    session = get_object_or_404(Session, id=session_id, tutor__user=request.user)
    session.delete()
    return redirect('dashboard')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = TutorProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            tutor = profile_form.save(commit=False)
            tutor.user = user
            tutor.save()

            login(request, user)
            return redirect('dashboard')
    else:
        user_form = UserRegistrationForm()
        profile_form = TutorProfileForm()

    return render(request, 'tutoring/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

