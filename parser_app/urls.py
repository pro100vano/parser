from django.urls import path
from parser_app import views

app_name = 'parser'


urlpatterns = [
    path('start/', views.StartParser.as_view(), name="start")
]
