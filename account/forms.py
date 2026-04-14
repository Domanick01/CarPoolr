import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from .models import User 

class CustomUserRegistrationForm(UserCreationForm):
    """
    Custom registration form with email validation, password strength,
    and unique username checking
    """
    username = forms.CharField(
         max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    
    email = forms.EmailField(
        required=True,
        validators=[EmailValidator(message="Please enter a valid email address")],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address'
        })
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name'
        })
    )
    
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone number (optional)'
        })
    )
    
    age = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class' : 'form-control',
            'placeholder' : 'Age'
        })
    )
    
    driver_status = forms.ChoiceField(
    choices=[('False', 'I am a passenger'), ('True', 'I am a driver')],
    widget=forms.Select(attrs={'class': 'form-control'}),
    label="I am a..."
)
    
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'driver_status', 'phone_number', 'password1', 'password2'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    
    def clean_username(self):
        """
        Validate username uniqueness and format
        """
        username = self.cleaned_data.get('username')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken.')
        
        # Check username format (alphanumeric and underscores only)
        if not re.match(r'^[\w]+$', username):
            raise ValidationError(
                'Username can only contain letters, numbers, and underscores.'
            )
        
        # Check minimum length
        if len(username) < 3:
            raise ValidationError('Username must be at least 3 characters long.')
        
        return username
    
    def clean_email(self):
        """
        Validate email uniqueness and require .edu domain
        """
        email = self.cleaned_data.get('email')

        email = email.lower()

        if not email.endswith('.edu'):
            raise ValidationError('Only .edu email addresses are allowed.')

        if User.objects.filter(email=email).exists():
            raise ValidationError('An account with this email already exists.')

        return email

    def clean_password1(self):
        """
        Validate password strength beyond Django's default validators
        """
        password = self.cleaned_data.get('password1')
        
        # Check minimum length
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                'Password must contain at least one uppercase letter.'
            )
        
        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                'Password must contain at least one lowercase letter.'
            )
        
        # Check for at least one digit
        if not re.search(r'\d', password):
            raise ValidationError('Password must contain at least one number.')
        
        # Check for at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                'Password must contain at least one special character (!@#$%^&*(),.?":{}|<>).'
            )
        
        return password
    
    def clean_phone_number(self):

        phone = self.cleaned_data.get('phone_number')

        if not phone:
            return None

        # Remove spaces and dashes
        phone = phone.replace(' ', '').replace('-', '')

        # Check if it contains only digits and optional + at the start
        if not re.match(r'^\+?\d{10,15}$', phone):
            raise ValidationError(
                'Please enter a valid phone number (10-15 digits).'
            )

        # Check uniqueness
        if User.objects.filter(Phone_Number=phone).exists():
            raise ValidationError(
                'An account with this phone number already exists.'
            )

        return phone
    
    def save(self, commit=True):
        '''Saves user with hashed password'''
        user = super().save(commit=False)  # get the user instance
        user.email = self.cleaned_data['email']
        user.Age = self.cleaned_data.get('age')
        user.Phone_Number = self.cleaned_data.get('phone_number') or None
        user.Driver_Status = self.cleaned_data.get('driver_status') == 'True'        
        if commit:
            user.save()  # saves the user including the hashed password
        return user
