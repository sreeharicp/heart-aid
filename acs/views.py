from __future__ import absolute_import
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.views import generic
from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy

from .forms import RegistrationForm, LoginForm, PatientForm, TempPatientDataForm, LabReportForm, PatientApptForm

from django.template import RequestContext
from django.views.generic import ListView
from django.template import RequestContext
from django.views.generic import ListView

from .models import PermissionsRole, Patient, TempPatientData, Alert, Doctor, LabReport, PatientAppt

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404,redirect
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
import datetime

STAFF_APPROVAL_ROLES = ('admin', 'doctor', 'staff', 'nurse', 'lab')

def HomePageView(request):



	#Model Definitions & Declarations
	permissionModel = PermissionsRole
	patientModel = Patient

	#temp data for the user has been found
	tempDataFound = 0

	#Assign default permission role
	permissionRoleForUser = 'pending'
	medications_for_patient = ""

	#Assign a default approval rating
	approval = 0

	#Assign a default authentication boolean
	authenticated = False

	# approvalSwitch = 0

	#Check to see if the user has logged into the system or not
	if request.user.is_authenticated():

		#Boolean to ensure valid request authentication
		authenticated = True

		#Attempt a DB query on the request object
		if permissionModel.objects.filter(user__username=request.user.username)[:1].exists():

			#If request object from query exists, create a variable assignment on that object
			permissionRoleForUser = permissionModel.objects.filter(user__username=request.user.username)[:1].get()

			#If the logged in person is a patient, grab request object, make a query and grab the approval integer
			if patientModel.objects.filter(user__username=request.user.username)[:1].exists():

				#Get an integer declaraction for the approval of the user
				approvalSwitch = patientModel.objects.filter(user__username=request.user.username)[:1].get()

			#If the person is a hospital member, then they will automatically be considered approved
			if (permissionRoleForUser.role in STAFF_APPROVAL_ROLES):
				approval = 1
			else:
				if patientModel.objects.filter(user__username=request.user.username)[:1].exists():
					approval = approvalSwitch.approved
				else:
					approval = 0

	#Under the instance that the user is not authenticated
	else:
		permissionRoleForUser = ""



	return render( request, 'index.html', {'permissionModel': permissionModel, 'user': request.user, 'roles': permissionRoleForUser, 'approval': approval, 'authenticated': authenticated})



def SuccessTestView(request):
	return render(request, 'accounts/success.html')

def index2(request):
	return render(request, 'accounts/index2.html')

class SuccessPageView(generic.TemplateView):
	template_name = 'accounts/success.html'

class SuccessFormPageView(generic.TemplateView):
	template_name = 'accounts/formsuccess.html'

class SignUpView(generic.CreateView):

	form_class = RegistrationForm
	model = User
	template_name = 'register.html'
	success_url = reverse_lazy('Success')


'''''''''''''''''''''''''''''''''''''''''''''''''''
Login view for the user to redirect into the patient/admin portal
'''''''''''''''''''''''''''''''''''''''''''''''''''

class LoginView(generic.FormView):
	form_class = LoginForm
	success_url = reverse_lazy('Portal')
	template_name = 'login.html'

	def form_valid(self, form):
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username=username, password=password)

		if user is not None and user.is_active:
			login(self.request, user)
			return super(LoginView, self).form_valid(form)
		else:
			return self.invalid(form)


def PatientPortalView(request):
	# template_name = 'home.html'
	#Model Definitions & Declarations
	permissionModel = PermissionsRole
	patientModel = Patient
	userModel = User
	tempModel = TempPatientData
	conditions_complete = False
	patient_model = Patient
	alert_model = Alert

	approvalSwitch = 0

	#Assign default permission role
	permissionRoleForUser = 'pending'

	#Assign a default approval rating
	approval = 0

	#Assign a default authentication boolean
	authenticated = False

	patient = -1


	#If user has already sent an alert request
	alert_sent = 0

	#Check to see if the user has logged into the system or not
	if request.user.is_authenticated():

		if patient_model.objects.filter(user=request.user.id)[:1].exists():
			patient = patient_model.objects.filter(user=request.user.id)[:1].get()

			if Alert.objects.filter(alert_patient=patient)[:1].exists():
				alert_sent = 1
				patient.alertSent = 1
				patient.save()
			else:
				alert_sent = patient.alertSent


		#Boolean to ensure valid request authentication
		authenticated = True

		#Attempt a DB query on the request object
		if permissionModel.objects.filter(user=request.user.id)[:1].exists():

			#If request object from query exists, create a variable assignment on that object
			permissionRoleForUser = permissionModel.objects.filter(user=request.user.id)[:1].get()

			#If the logged in person is a patient, grab request object, make a query and grab the approval integer
			if patientModel.objects.filter(user=request.user.id)[:1].exists():

				#Get an integer declaraction for the approval of the user
				approvalSwitch = patientModel.objects.filter(user=request.user.id)[:1].get()

			#If the person is a hospital member, then they will automatically be considered approved
			if (permissionRoleForUser.role in STAFF_APPROVAL_ROLES):
				approval = 1
			else:
				approval = approvalSwitch.approved

	#Under the instance that the user is not authenticated
	else:
		permissionRoleForUser = ""

	tempUserInformation = ""
	if tempModel.objects.filter(user=request.user.id)[:1].exists():
		tempUserInformation = tempModel.objects.filter(user=request.user)[:1].get()

	form = TempPatientDataForm()

	if request.method == "POST":

		form = TempPatientDataForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.data_sent = 1
			instance.email_address = request.user.username
			instance.save()
			return HttpResponseRedirect('formsuccess')


	doc_name = ''
	appts = ''
	if (not permissionRoleForUser == 'pending' and permissionRoleForUser.role == 'doctor'):

		doc_obj = Doctor.objects.filter(doctor_user=request.user).get()

		doc_name = doc_obj.doctor_first_name + ' ' + doc_obj.doctor_last_name

		appts = PatientAppt.objects.filter(doctor=doc_obj).count()

		if appts == 0:
			appts = 'No Appointments'

	current_patient = ''

	if (not tempUserInformation == ''):
		if (Patient.objects.filter(fill_from_application=tempUserInformation).exists()):
			current_patient = Patient.objects.filter(fill_from_application=tempUserInformation).get()

	#Query all the people that have alert sent
	get_all_unapproved_patients = TempPatientData.objects.filter(data_sent=1).all()

	unapproved_patient_list = []
	temp_patient_data_list = []


	for each_patient in get_all_unapproved_patients:
		if (not Patient.objects.filter(fill_from_application = each_patient).exists()):
			unapproved_patient_list.append(each_patient)

	unapproved_count = len(unapproved_patient_list)

	if not permissionRoleForUser == "pending":
		if permissionRoleForUser.role == 'patient':
			patient_date_time_set = Patient.objects.filter(fill_from_application__user=request.user).get()
			#print patient_date_time_set.date_created
			if patient_date_time_set.date_created == '9-20-1995':
				d = datetime.date.today()
				user_date_add = datetime.datetime.now()
				#print ' is now'
				patient_date_time_set.date_created = user_date_add
				patient_date_time_set.save()


	context = {

		'form': form,
		'permissionModel': permissionModel,
		'user': request.user,
		'roles': permissionRoleForUser,
		'approval': approval,
		'authenticated': authenticated,
		'temp_user_data': tempUserInformation,
		'doc_name' : doc_name,
		'current_patient' : current_patient,
		'unapproved_patient_list' : unapproved_patient_list,
		'unapproved_count' : unapproved_count,

	}

	return render(request, 'portal.html', context)


def logout_user(request):
	logout(request)
	return HttpResponseRedirect(reverse_lazy('Home'))

def PatientSearch(request):

	user_has_been_located = False

	patient_model = Patient #Perform queries on the database model that holds all the patient information

	search_data_list = ""

	patient_found = ''

	#Grab the post param information so that you can perform iteration logic through the database on the searchable customer
	if request.method == "POST":
		search_data = request.POST.get("search_data", "") #store the data of the user search information into a variable that you can parse
		db_search_type = request.POST.get("db_search_type", "")

		search_data_list = search_data.split(" ") #If there is more than one entry in the search bar, parse it as necessary

		#Check to see if the inputted email matches any of the patient emails in the databases
		if db_search_type == "email":
			if patient_model.objects.filter(fill_from_application__email_address__iexact=search_data_list[0]).exists():
				patient_found = patient_model.objects.filter(fill_from_application__email_address__iexact=search_data_list[0]).get()
				search_data_list.append(patient_found)
				user_has_been_located = True

		elif db_search_type == "firstlast":
			if patient_model.objects.filter(fill_from_application__first_name__iexact=search_data_list[0]).exists() and patient_model.objects.filter(fill_from_application__last_name__iexact=search_data_list[1]).exists():
				patient_found = patient_model.objects.filter(fill_from_application__first_name__iexact=search_data_list[0], fill_from_application__last_name__iexact=search_data_list[1]).all()
				search_data_list.append(patient_found)
				user_has_been_located = True

	if search_data_list == "":

		context = {

			'search_data': 'none',
			'located': user_has_been_located
		}

	elif user_has_been_located == True:


		context = {

			'search_data': search_data_list,
			'temp_user_data': patient_found,
			'located': user_has_been_located
		}

	else:

		context = {

			'search_data': search_data_list,
			'temp_user_data': patient_found,
			'located': user_has_been_located
		}

	return render(request, 'search.html', context)

def ProcessPatientApproval(request):

	#Query the temp_patient_data from the primary key
	if request.method == "POST" and 'pk_pending' in request.POST:
		primary_key_val = request.POST.get('pk_pending', '')
		#print primary_key_val
		temp_object = TempPatientData.objects.filter(user_id=primary_key_val).get()

		#Create a new patient object
		p = Patient.objects.create(fill_from_application=temp_object, user=temp_object.user, approved=1, alertSent=0)
		p.save()

		r = PermissionsRole.objects.create(role='patient', user=temp_object.user)
		r.save()


	return HttpResponseRedirect(reverse("PatientApprovalView"))

def PatientApprovalView(request):

	#Query all the people that have alert sent
	get_all_unapproved_patients = TempPatientData.objects.filter(data_sent=1).all()

	unapproved_patient_list = []
	temp_patient_data_list = []


	for each_patient in get_all_unapproved_patients:
		if (not Patient.objects.filter(fill_from_application = each_patient).exists()):
			unapproved_patient_list.append(each_patient)

	unapproved_count = len(unapproved_patient_list)

	context = {

		'unapproved_patient_list' : unapproved_patient_list,
		'size_of' : len(unapproved_patient_list)

	}

	return render(request, 'approval1.html', context)

def CreateLabReportView(request):

	title = "Lab Report Creation Form"
	form = LabReportForm(request.POST or None)

	if form.is_valid():
		instance = form.save(commit=False)

		instance.save()
		return HttpResponseRedirect('formsuccess')


	context = {
		"form": form,
		"template_title": title,
	}
	return render(request, 'create_report.html', context)


def get_lab_results(request):

	#This view is going to be responsible for getting all the lab results and description for each patient
	if request.method == "POST" and 'patient_labs' in request.POST:

		#We need to get all the lab results based on the patient PRIMARY KEY
		patient_labs = request.POST.get("patient_labs", "")
		patient_labs = int(patient_labs)

		patient_lab_results = LabReport.objects.filter(lab_patient__id=patient_labs).all()

		current_patient = Patient.objects.filter(id=patient_labs).get()

		context = {

			'patient_lab_results' : patient_lab_results,
			'current_patient' : current_patient
		}

		return render(request,'labresults.html', context)
	else:
		return HttpResponseRedirect(reverse("Portal"))

def display_all_lab_results(request):

	#Query all the lab reports in the system into an object to loop and display for

	all_lab_tests = LabReport.objects.all()


	if PermissionsRole.objects.filter(user__username=request.user.username)[:1].exists():
		roles = PermissionsRole.objects.filter(user__username=request.user.username)[:1].get()

	#print all_lab_tests

	context = {

		'all_lab_tests' : all_lab_tests,
		'roles' : roles
	}

	return render(request,'all_lab_results.html', context)

def delete_lab_results(request):

	if request.method == "POST" and "report_remove" in request.POST:

		lab_found = request.POST.get("report_remove", "")

		delete_this_lab = LabReport.objects.filter(pk=lab_found).get()
		delete_this_lab.delete()

		all_lab_tests = LabReport.objects.all()

		context = {

			'all_lab_tests' : all_lab_tests
		}

		return render(request,'all_lab_results.html', context)

def edit_lab_results(request):

	primary_key_val = ""

	if request.method == "POST" and "report_remove" in request.POST:

		lab_found = request.POST.get("report_remove", "")

		model_instance = LabReport.objects.get(pk=lab_found)

		#print 'The current lab model that has been found is: \n'
		#print model_instance

		primary_key_val = model_instance

		patient_object = model_instance.lab_patient

		form = LabReportForm(instance=model_instance)

		context = {
			'form' : form,
			'patient_object' : patient_object,
		}

		return render(request,'edit_lab_report.html', context)


	elif request.method == "POST" and "send_form" in request.POST:

		patient_id_key = request.POST.get('pk_patient2', '')
		# TempPatientData.objects.filter(id = 'pk_patient2').get()
		patient_id_key = int(patient_id_key)

		instance = get_object_or_404(LabReport, id=patient_id_key)

		form = LabReportForm(request.POST or None, instance=instance)
		if form.is_valid():
			form.save()

		return HttpResponseRedirect('formsuccess')


	elif request.method == "POST":


		form = LabReportForm(request.POST, instance=primary_key_val)

		context = {
			'form' : form
		}

		if form.is_valid():

			form.save()
			return HttpResponseRedirect('/accounts/portal/')

		return render(request,'all_lab_results.html', context)




def UpdateAccountView(request):
	title = "Update Account Information"
	form = TempPatientDataForm(request.POST or None)
	patient_model = Patient


	patient = patient_model.objects.filter(user=request.user)[:1].get()

	if (TempPatientData.objects.filter(user=request.user)[:1].exists()):

		instance = TempPatientData.objects.filter(user=request.user)[:1].get()
		form = TempPatientDataForm(instance = instance)

	if request.method == "POST":

		TPD = TempPatientData.objects.filter(user=request.user)[:1].get()

		if (not TPD is None):
			instance = TempPatientData.objects.filter(user=request.user)[:1].get()

			# form = TempPatientDataForm(request.POST, instance = instance)

		form = TempPatientDataForm(request.POST, instance = TPD)
		if form.is_valid():

			form.save()

		return HttpResponseRedirect('/accounts/portal/update_account/')


	context = {
		"form": form,
		"template_title": title
	}
	return render(request, 'update_account.html', context)



def DeleteUser(request):

	patient_model = Patient

	if request.method == "POST":
		pk_id = request.POST.get("pk", "")
		if patient_model.objects.filter(id=pk_id).exists():
			found_patient_object = patient_model.objects.filter(id=pk_id).get()
			found_patient_object.delete()

	context = {

		'pk_id': pk_id
	}

	return render(request, 'deleted.html', context)



def get_lab_results(request):

	#This view is going to be responsible for getting all the lab results and description for each patient
	if request.method == "POST" and 'patient_labs' in request.POST:

		#We need to get all the lab results based on the patient PRIMARY KEY
		patient_labs = request.POST.get("patient_labs", "")
		patient_labs = int(patient_labs)

		patient_lab_results = LabReport.objects.filter(lab_patient__id=patient_labs).all()

		current_patient = Patient.objects.filter(id=patient_labs).get()

		context = {

			'patient_lab_results' : patient_lab_results,
			'current_patient' : current_patient
		}

		return render(request,'labresults.html', context)
	else:
		return HttpResponseRedirect(reverse("Portal"))




def PatientDataView(request):

	#get permissions of current user
	roles = PermissionsRole.objects.filter(user=request.user)[:1].get()

	patients = ''

	if roles.role == 'doctor':
		current_doctor = Doctor.objects.filter(doctor_user=request.user)

		if PatientAppt.objects.filter(doctor=current_doctor).exists():

			patients = PatientAppt.objects.filter(doctor=current_doctor).all()
			if PatientAppt.objects.filter(doctor=current_doctor).count() == 0:
				patients = 0

			final_patient_list = []
			final_patient_users = []

			for patient in patients:
				if patient.user.user not in final_patient_users:
					final_patient_users.append(patient.user.user)
					final_patient_list.append(patient)

			patients = final_patient_list

		else:
			patients = 0



	context = {

		'roles' : roles,
		'patients' : patients

	}

	return render(request, 'view_patients.html', context)


def ViewAllPatientData(request):

	temp_patient_data = Patient.objects.all()

	#print temp_patient_data

	context = {

		'temp_user_data' : temp_patient_data
	}

	return render(request, 'view_all_patient_data_hsp.html', context)



def GenerateStatsView(request):


	roles = PermissionsRole.objects.filter(user=request.user.id)[:1].get()
	# roles = "doctor"

	#GENDER
	total_patients = TempPatientData.objects.filter().count()

	num_males = (float(TempPatientData.objects.filter(gender='male').count())/float(total_patients))*100
	num_females = (float(TempPatientData.objects.filter(gender='female').count())/float(total_patients))*100
	num_other = (float(TempPatientData.objects.filter(gender='other').count())/float(total_patients))*100
	num_PNTS = (float(TempPatientData.objects.filter(gender='prefer not to say').count())/float(total_patients))*100
	num_males = format(num_males, '.2f')
	num_females = format(num_females, '.2f')
	num_other = format(num_other, '.2f')
	num_PNTS = format(num_PNTS, '.2f')

	#AGE
	age_1 = (float(TempPatientData.objects.filter(age__range=(0,19)).count())/float(total_patients))*100
	age_1 = format(age_1, '.2f')

	age_2 = (float(TempPatientData.objects.filter(age__range=(19,45)).count())/float(total_patients))*100
	age_2 = format(age_2, '.2f')

	age_3 = (float(TempPatientData.objects.filter(age__range=(45,61)).count())/float(total_patients))*100
	age_3 = format(age_3, '.2f')

	age_4 = (float(TempPatientData.objects.filter(age__range=(61,130)).count())/float(total_patients))*100
	age_4 = format(age_4, '.2f')

	#HOSPITAL CASES RESOLVED
	total_cases = PatientAppt.objects.filter().count()


	staff_roles = PermissionsRole.objects.exclude(role="patient").count()


	#print 'Accepted: %d and accepted_count_last_30_days: %d\n' %(all_accepted, accepted_count_last_30_days)

	context = {

		'roles' : roles,
		'num_males' : num_males,
		'num_females' : num_females,
		'num_other' : num_other,
		'num_PNTS' : num_PNTS,
		'total_patients' : total_patients,

		'age_1' : age_1,
		'age_2' : age_2,
		'age_3' : age_3,
		'age_4' : age_4,

		'staff_roles' : staff_roles
	}

	return render(request, 'stats.html', context)
