from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from .models import Patient, TempPatientData, LabReport, PatientAppt
from django.db import models
from django import forms

#forms.ModelForm



class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Patient Email Address"
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password1',
            'password2',
            ButtonHolder(
                Submit('register', 'Register', css_class='btn-primary')
            )
        )

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Email Address"
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            ButtonHolder(
                Submit('login', 'Login', css_class='btn-primary')
            )
        )

class PatientForm(forms.ModelForm):
    user = forms.CharField(max_length=40)
    class Meta:
        model = Patient
        fields = '__all__'


class LabReportForm(forms.ModelForm):
    class Meta:
        model = LabReport
        # widgets = {
        #     'medication_name': forms.TextInput(attrs={'placeholder': 'Enter the name of the medication'}),
        # }
        fields = '__all__'



class TempPatientDataForm(forms.ModelForm):
    class Meta:
        model = TempPatientData
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Legal First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Legal Last Name'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '+1(areacode)(phone-number)'}),
            'DOB': forms.TextInput(attrs={'placeholder': '01/01/2000'}),
            #'ssn': forms.TextInput(attrs={'placeholder': '111223333'}),
            #'allergies': forms.TextInput(attrs={'placeholder': 'Separate your allergies by commas'}),
            #'medications': forms.TextInput(attrs={'placeholder': 'Separate your medications by commas'}),
            #'insurance_policy_number': forms.TextInput(attrs={'placeholder': 'Valid Insurance Required'}),
            'address': forms.TextInput(attrs={'placeholder': 'address'}),
            'heart_rate': forms.TextInput(attrs={'placeholder': 'heart_rate'}),
            'systolic_blood_pressure': forms.TextInput(attrs={'placeholder': 'systolic_blood_pressure'}),
            'CHF': forms.TextInput(attrs={'placeholder': 'CHF'}),
            'creatinine': forms.TextInput(attrs={'placeholder': 'creatinine'}),
            'cardiac_arrest': forms.TextInput(attrs={'placeholder': 'cardiac_arrest'}),
            'biomarkers': forms.TextInput(attrs={'placeholder': 'biomarkers'}),
            'st_elev': forms.TextInput(attrs={'placeholder': 'st_elev'}),


        }
        fields = '__all__'
        exclude = ['user', 'data_sent', 'email_address']



class PatientApptForm(forms.ModelForm):
    class Meta:
        model = PatientAppt
        fields = '__all__'
        exclude = ['user']
