from django.urls import path, include
from main_app import views


app_name = 'main'

targets = [
    path('list/', views.TargetsList.as_view(), name='list'),
    path('create/', views.CreateTarget.as_view(), name='create'),
    path('edit/<int:pk>/', views.EditTarget.as_view(), name='edit')
]

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('targets/', include((targets, "targets"))),
    path('reminder/', views.Reminder.as_view(), name='reminder'),
    path('settings/', views.Settings.as_view(), name='settings'),
    path('documentation/', views.Documentation.as_view(), name='documentation'),
    path('webhook/', views.TgHooks.as_view(), name='tg_hook'),
]
