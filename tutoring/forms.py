from django import forms
from .models import Student, Session, Tutor
from django.contrib.auth.models import User


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'age']

class SessionForm(forms.ModelForm):
    duration = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter duration in minutes'}),min_value=1, error_messages={'min_value': 'Duration must be at least 1 minute.'})
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'placeholder': 'YYYY-MM-DD',
            'type': 'date'  
        }),
        input_formats=['%Y-%m-%d'], 
        error_messages={'invalid': 'Enter a valid date.'}
    )
    class Meta:
        model = Session
        fields = ['student', 'date', 'duration', 'topic']


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            self.add_error("password_confirm", "Passwords do not match.")

class TutorProfileForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = ['bio']
