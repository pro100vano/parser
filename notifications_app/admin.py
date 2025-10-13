from django.contrib import admin

from notifications_app.models import NotificationModel, TgAccounts


class NotificationModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'has_seen', 'date_created', 'message')


admin.site.register(NotificationModel, NotificationModelAdmin)
admin.site.register(TgAccounts)
