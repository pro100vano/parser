from django.utils import timezone
from django.db import transaction
from parser_app.models import TargetsModel, TargetSettingsModel


class ParserRepository:

    def __init__(self, user=None, **kwargs):
        if user is not None:
            self.user = user
        elif kwargs.get('user', None) is not None:
            self.user = kwargs.get('user')

    def create_target(self, title, url, target_type=TargetsModel.SIMPLE, params=None):
        with transaction.atomic():
            target = TargetsModel.objects.create(
                user=self.user,
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
                    )

    def edit_target(self, pk, title, url, target_type=TargetsModel.SIMPLE, params=None):
        with transaction.atomic():
            try:
                target = TargetsModel.objects.get(user=self.user, pk=pk)
            except TargetsModel.DoesNotExist:
                return
            target.title = title
            target.url = url
            target.type = int(target_type)
            target.save()
            if int(target_type) == TargetsModel.DIFFICULT and params is not None:
                target.settings.all().delete()
                for setting in params:
                    TargetSettingsModel.objects.create(
                        target=target,
                        type=int(setting.get('checking_type')),
                        type_param=setting.get('type_param', ''),
                        block=setting.get('block'),
                    )

    def get_target(self, pk):
        try:
            return TargetsModel.objects.get(user=self.user, pk=pk)
        except Exception as e:
            print(e)
            return None

    def get_targets_list_count(self):
        return TargetsModel.objects.filter(user=self.user).count()

    def get_targets_list(self):
        return TargetsModel.objects.filter(user=self.user)

    def get_active_targets_list_count(self):
        return TargetsModel.objects.filter(user=self.user, activate=True).count()

    def get_active_targets_list(self):
        return TargetsModel.objects.filter(user=self.user, activate=True)

    @staticmethod
    def change_status(target, target_status):
        target.status = target_status
        target.status_changed = timezone.now()
        target.save()

    def toggle_target(self, target_pk):
        target = TargetsModel.objects.get(user=self.user, pk=target_pk)
        target.activate = not target.activate
        target.save()

    def remove_target(self, target_pk):
        TargetsModel.objects.get(user=self.user, pk=target_pk).delete()

    @staticmethod
    def get_types():
        return TargetsModel.TARGET_TYPE

    @staticmethod
    def get_checking_types():
        return TargetSettingsModel.CHECKING_TYPE
