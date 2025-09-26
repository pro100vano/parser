from django.utils import timezone
from django.db import transaction
from parser_app.models import TargetsModel, TargetSettingsModel


class ParserRepository:

    def __init__(self, **kwargs):
        if kwargs.get('user', None) is not None:
            self.user = kwargs.get('user')

    @staticmethod
    def create_target(title, url, target_type=TargetsModel.SIMPLE, params=None):
        with transaction.atomic():
            target = TargetsModel.objects.create(
                title=title,
                url=url,
                type=int(target_type)
            )
            if int(target_type) == TargetsModel.DIFFICULT and params is not None:
                for setting in params:
                    TargetSettingsModel.objects.create(
                        target=target,
                        type=int(setting.get('checking_type')),
                        type_param=setting.get('type_param', ''),
                        block=setting.get('block'),
                        message=''
                    )

    @staticmethod
    def get_targets_list():
        return TargetsModel.objects.all()

    @staticmethod
    def get_active_targets_list():
        return TargetsModel.objects.filter(activate=True)

    @staticmethod
    def change_status(target, target_status):
        target.status = target_status
        target.status_changed = timezone.now()
        target.save()

    @staticmethod
    def toggle_target(target_pk):
        target = TargetsModel.objects.get(pk=target_pk)
        target.activate = not target.activate
        target.save()

    @staticmethod
    def remove_target(target_pk):
        TargetsModel.objects.get(pk=target_pk).delete()

    @staticmethod
    def get_types():
        return TargetsModel.TARGET_TYPE

    @staticmethod
    def get_checking_types():
        return TargetSettingsModel.CHECKING_TYPE
