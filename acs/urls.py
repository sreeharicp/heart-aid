"""django_1_11_updated URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""


from django.contrib import admin

from django.conf.urls import include, url

from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^super/', include(admin.site.urls)),
    url(r'^$', HomePageView, name='Home'),
    url(r'success_test/$', SuccessTestView, name='SuccessTestView'),
    url(r'success/$', SuccessPageView.as_view(), name='Success'),
    url(r'formsuccess/$', SuccessFormPageView.as_view(), name="DataSubmitted"),
    url(r'accounts/apply/$', SignUpView.as_view(), name="Signup"),
    url(r'accounts/login/$', LoginView.as_view(), name="Login"),
    url(r'^accounts/portal/$', PatientPortalView, name="Portal"),
    url(r'logout/$', logout_user, name="Logout"),
    url(r'^search/$', PatientSearch, name="PatientSearch"),
    url(r'^accounts/portal/hsp/approvals$', PatientApprovalView, name="PatientApprovalView"),
    url(r'^accounts/portal/hsp/approvals/approve$', ProcessPatientApproval, name="ProcessPatientApproval"),
    url(r'^accounts/portal/admin/create_lab_report$', CreateLabReportView, name="CreateLabReportView"),
    url(r'^accounts/portal/update_account/$', UpdateAccountView, name="Update"),
    url(r'^delete/$', DeleteUser, name="DeleteUser"),
    url(r'^accounts/portal/admin/view_lab_results$', get_lab_results, name="get_lab_results"),
    url(r'^accounts/portal/admin/view_patients$', PatientDataView, name="PatientDataView"),
    url(r'^accounts/portal/admin/view_all_patient_data$', ViewAllPatientData, name="ViewAllPatientData"),
    url(r'^accounts/portal/admin/generate$', GenerateStatsView, name="GenerateStats"),
    url(r'^accounts/portal/index2/$', index2, name="index2"),
    url(r'^accounts/portal/admin/all_lab_tests$', display_all_lab_results, name="display_all_lab_results"),
    url(r'^accounts/portal/admin/delete_lab_report$', delete_lab_results, name="delete_lab_results"),
    url(r'^accounts/portal/admin/edit_lab_report$', edit_lab_results, name="edit_lab_results"),

]
