from django.urls import path
from parser_app import views

app_name = 'parser'


urlpatterns = [
    path('start/', views.StartParser.as_view(), name="start"),

    path('<int:pk>/activate/toggle/', views.ToggleTarget.as_view(), name='activate_toggle'),
    path('<int:pk>/remove/', views.RemoveTarget.as_view(), name='remove_target')
]
