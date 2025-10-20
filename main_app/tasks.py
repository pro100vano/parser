from celery import shared_task
from django.contrib.auth.models import User

from parser_app.repositories import ParserRepository
from parser_app.utils import Parser


@shared_task(name="parser_start")
def parser_start(user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        pass
    else:
        targets = ParserRepository(user).get_active_targets_list()
        Parser(user).start_parser(targets)
    return True
