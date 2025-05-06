from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import AlumniProfile, School

class UserRegisterForm(UserCreationForm):
    """Form for user registration"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        # Add placeholders and styles to form fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
            self.fields[field_name].widget.attrs.update({'placeholder': field_name.replace('_', ' ').capitalize()})
            
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

class CustomLoginForm(AuthenticationForm):
    """Custom authentication form with styling"""
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        # Add placeholders and styles to form fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
            self.fields[field_name].widget.attrs.update({'placeholder': field_name.replace('_', ' ').capitalize()})

class AlumniProfileForm(forms.ModelForm):
    """Form for alumni profile creation/editing"""
    class Meta:
        model = AlumniProfile
        exclude = ['user', 'status', 'created_at', 'updated_at']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'graduation_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'degree': forms.TextInput(attrs={'class': 'form-control'}),
            'major': forms.TextInput(attrs={'class': 'form-control'}),
            'current_company': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin_profile': forms.URLInput(attrs={'class': 'form-control'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def clean_graduation_year(self):
        year = self.cleaned_data.get('graduation_year')
        if year and (year < 1950 or year > 2030):
            raise forms.ValidationError("Please enter a valid graduation year between 1950 and 2030.")
        return year
    
    def clean_linkedin_profile(self):
        url = self.cleaned_data.get('linkedin_profile')
        if url and not ('linkedin.com' in url):
            raise forms.ValidationError("Please enter a valid LinkedIn profile URL.")
        return url

class SchoolForm(forms.ModelForm):
    """Form for school creation/editing (admin only)"""
    class Meta:
        model = School
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

class AlumniStatusForm(forms.ModelForm):
    """Form for changing alumni status (admin only)"""
    class Meta:
        model = AlumniProfile
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }