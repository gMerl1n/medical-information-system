from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('users/register/patient', views.RegistrationPatientAPIView.as_view(), name='register_patient'),
    path('users/login/patient', views.LoginPatientAPIView.as_view(), name='login_patient'),
    path('users/register/doctor', views.RegistrationDoctorAPIView.as_view(), name='register_doctor'),
    path('users/login/doctor', views.LoginDoctorAPIView.as_view(), name='login_doctor'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
