# -*- coding: utf-8 -*-
from __future__ import unicode_literals


# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
import datetime


class Doctor(models.Model):
    doctor_first_name = models.CharField(max_length=256, default="")
    doctor_last_name = models.CharField(max_length=256, default="")
    doctor_user = models.OneToOneField(User, unique=True, blank=False, default="", null=False, on_delete=models.CASCADE)
    def __unicode__(self):
    	return("Dr. " + str(self.doctor_first_name.title()) + ' ' + str(self.doctor_last_name.title()))


class LabTech(models.Model):
    lab_first_name = models.CharField(max_length=256, default="")
    lab_last_name = models.CharField(max_length=256, default="")
    lab_user = models.OneToOneField(User, unique=True, blank=False, default="", null=False ,on_delete=models.CASCADE)



    def __unicode__(self):
    	return(str(self.lab_first_name) + ' ' + str(self.lab_last_name))

class PermissionsRole(models.Model):
    role = models.CharField(max_length=256, choices=[('admin', 'admin'), ('nurse', 'nurse'), ('staff', 'staff'), ('doctor', 'doctor'), ('patient', 'patient'), ('lab', 'lab')])
    user = models.OneToOneField(User, unique=True, blank=True, default="" ,on_delete=models.CASCADE)

    def __unicode__(self):
    	return(str(self.role))


class TempPatientData(models.Model):

    user = models.OneToOneField(User,unique=True,null=True,default="",on_delete=models.CASCADE)
    email_address = models.CharField(max_length=256, blank=False)
    first_name = models.CharField(max_length=256, default="")
    last_name = models.CharField(max_length=256, default="")
    age = models.IntegerField(default = 18, blank=False)
    gender = models.CharField(max_length=256, choices=[('male','Male'), ('female', 'Female'), ('other', 'Other'), ('prefer not to say', 'Prefer Not To Say')], default='Select a gender', blank = False)
    phone_number = PhoneNumberField(blank = True, default="")
    # DOB = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    DOB = models.CharField(max_length=255, blank=True, null=True)
    #allergies = models.CharField(max_length=256, default="")
    address = models.CharField(max_length=256, default="")
    #medications = models.CharField(max_length=256, default="")
    heart_rate = models.IntegerField(default = 72, blank=False)
    systolic_blood_pressure = models.IntegerField(default = 120, blank=False)
    CHF = models.CharField(max_length=256, choices=[('No CHF','No CHF'),('Rales and/or JVD','Rales and/or JVD'),('Pulmonary edema','Pulmonary edema'),('Cardiogenic shock','Cardiogenic shock')], default='No CHF', blank = False)
    creatinine = models.DecimalField(max_digits=5,decimal_places=2,default = 0.5, blank=False)
    cardiac_arrest = models.CharField(max_length=256, choices=[('yes','Yes'), ('no','No')], default='no', blank = False)
    biomarkers = models.CharField(max_length=256, choices=[('yes','Yes'), ('no','No')], default='no', blank = False)
    st_elev = models.CharField(max_length=256, choices=[('yes','Yes'), ('no','No')], default='no', blank = False)

    data_sent = models.IntegerField(default=0)


    def __unicode__(self):
    	return(str(self.first_name) + " " + str(self.last_name) + " " + str(self.email_address))

class Patient(models.Model):

    fill_from_application = models.OneToOneField(TempPatientData,unique=True,null=True,default="",on_delete=models.CASCADE)
    user = models.OneToOneField(User, unique=True,  blank=True, default="", null=True,on_delete=models.CASCADE)
    approved = models.IntegerField(default=0, null=False)
    alertSent = models.IntegerField(default=0, null=False)
    date_created = models.CharField(default="11-3-2018", null=True, max_length=20)



    def __unicode__(self):
    	return('Email: ' + str(self.fill_from_application.email_address) + ' First Name: ' + str(self.fill_from_application.first_name) + ' Last Name: ' + str(self.fill_from_application.last_name))

class Alert(models.Model):
    alert_level = models.IntegerField(default=0, null=False)
    alert_patient = models.OneToOneField(Patient, unique = True, null = True,on_delete=models.CASCADE)
    alert_description = models.CharField(max_length=255, default="", null = True, unique=False)

class LabReport(models.Model):
    lab_patient = models.ForeignKey(Patient, default = "0",on_delete=models.CASCADE)
    #lab_results = models.CharField(max_length=255, choices=[('positive', 'Positive'), ('negative', 'Negative')])
    #lab_test = models.CharField(max_length=255, choices=[('Blood pressure screening', 'Blood pressure screening'),('biomarkers','biomarkers'),('CHF','CHF'),('creatinine','creatinine'),('st_elev','st_elev') ])
    lab_notes = models.TextField(default="Insert Notes For Lab Test")
    lab_tech = models.ForeignKey(LabTech, default="",on_delete=models.CASCADE)
    systolic_blood_pressure = models.IntegerField(default = 120, blank=False)
    CHF = models.CharField(max_length=256, choices=[('No CHF','No CHF'),('Rales and/or JVD','Rales and/or JVD'),('Pulmonary edema','Pulmonary edema'),('Cardiogenic shock','Cardiogenic shock')], default='No CHF', blank = False)
    creatinine = models.FloatField(default = 0.5, blank=False)
    cardiac_arrest = models.CharField(max_length=256, choices=[('yes','Yes'), ('no','No')], default='no', blank = False)
    biomarkers = models.CharField(max_length=256, choices=[('yes','Yes'), ('no','No')], default='no', blank = False)
    st_elev = models.CharField(max_length=256, choices=[('yes','Yes'), ('no','No')], default='no', blank = False)



class PatientAppt(models.Model):
	doctor = models.ForeignKey(Doctor, unique=False, default=-1)
	user = models.ForeignKey(Patient, unique=False, blank=True, default="")
    
	def __unicode__(self):
		return str(self.doctor)
