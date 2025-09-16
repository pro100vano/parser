from django.contrib import admin

from parser_app.models import TargetsModel, TargetSettingsModel

admin.site.register(TargetsModel)
admin.site.register(TargetSettingsModel)
