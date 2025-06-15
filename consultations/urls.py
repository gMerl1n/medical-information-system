from django.urls import path
from . import views


urlpatterns = [
    path('consultation/create', views.CreateConsultation.as_view(), name='create_consultation'),
    path('consultation/list', views.ListConsultations.as_view(), name='list_consultation'),
    path('consultation/<int:pk>/', views.ConsultationDetail.as_view(), name='consultation_detail'),
    path('consultation/update/<int:pk>', views.ConsultationUpdate.as_view(), name='consultation_update'),
    path('consultation/remove/<int:pk>', views.RemoveConsultation.as_view(), name='remove_consultation'),
]