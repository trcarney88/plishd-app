from django.urls import path
from .views import (
    AccomplishmentListView, 
    AccomplishmentDetailView, 
    AccomplishmentCreateView, 
    AccomplishmentUpdateView, 
    AccomplishmentDeleteView,
    CompanyAccomplishmentListView,
    JobTitleAccomplishmentListView,
    reports
)
from . import views
urlpatterns = [
    path('<str:username>/', AccomplishmentListView.as_view(), name='timeline'),
    path('accomplishment/<int:pk>/', AccomplishmentDetailView.as_view(), name='accomplishment-detail'),
    path('accomplishment/new/', AccomplishmentCreateView.as_view(), name='accomplishment-create'),
    path('accomplishment/<int:pk>/update/', AccomplishmentUpdateView.as_view(), name='accomplishment-update'),
    path('accomplishment/<int:pk>/delete/', AccomplishmentDeleteView.as_view(), name='accomplishment-delete'),
    path('accomplishment/<str:username>/company/<str:company>/', CompanyAccomplishmentListView.as_view(), name='company-accomplishment'),
    path('accomplishment/<str:username>/job_title/<str:jobtitle>/', JobTitleAccomplishmentListView.as_view(), name='jobtitle-accomplishment')
]
