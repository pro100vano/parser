from celery import shared_task
import time
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from parser_app.models import TargetSettingsModel


@shared_task(name="simple_parser")
def simple_parser(task_type):
    test_target = TargetSettingsModel.objects.last()
    test_target.message = "1"
    test_target.save()
    # time.sleep(int(task_type) * 10)
    # channel_layer = get_channel_layer()
    # async_to_sync(channel_layer.group_send)(
    #     f"user_1",
    #     {
    #         "type": "send_data",
    #         "data": {
    #             "func": "test",
    #         },
    #     }
    # )
    print('test')
    return True
