from django.urls import path
from notifications_app import views

app_name = 'notifications'


urlpatterns = [
    path('test/', views.Notification.as_view(), name="test"),
    path('test/tg/', views.NotificationTg.as_view(), name="test_tg"),

    path('list/', views.Notifications.as_view(), name='list'),
    path('read/<int:pk>/', views.ReadNotification.as_view(), name='read'),

    path('tg/add/', views.TgUserAdd.as_view(), name='tg_user_add'),
    path('tg/remove/<int:pk>/', views.TgUserRemove.as_view(), name='tg_user_remove'),
    # path('')
]
