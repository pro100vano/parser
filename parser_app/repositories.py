from parser_app.models import TargetsModel


class ParserRepository:

    def __init__(self, **kwargs):
        if kwargs.get('user', None) is not None:
            self.user = kwargs.get('user')

    @staticmethod
    def get_targets_list():
        return TargetsModel.objects.all()
