import json

from django.shortcuts import render
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.http import JsonResponse
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class StartParser(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        task = 'simple_parser'
        PeriodicTask.objects.create(
            name='Repeat test',
            task=task,
            interval=IntervalSchedule.objects.get(every=10, period='seconds'),
            args=json.dumps([1]),
            start_time=timezone.now(),
        )
        # task = create_task.delay(task_id)
        # return JsonResponse({"task_id": task.id}, status=202)
        return JsonResponse({"task": task}, status=200)

