from django.contrib import admin

from parser_app.models import TargetsModel, TargetSettingsModel, UserPeriodicTasksModel

admin.site.register(TargetsModel)
admin.site.register(TargetSettingsModel)
admin.site.register(UserPeriodicTasksModel)
