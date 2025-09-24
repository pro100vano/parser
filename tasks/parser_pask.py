# from celery import shared_task
# import time
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
#
#
# @shared_task(name="simple_parser")
# def simple_parser(task_type):
#     time.sleep(int(task_type) * 10)
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         f"user_1",
#         {
#             "type": "send_data",
#             "data": {
#                 "func": "test",
#             },
#         }
#     )
#     print('test')
#     return True
