from django.urls import path, include
from main_app import views


app_name = 'main'

targets = [
    path('list/', views.TargetsList.as_view(), name='list'),
    path('create/', views.CreateTarget.as_view(), name='create')
]

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('targets/', include((targets, "targets"))),
]
