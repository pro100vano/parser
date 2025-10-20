import json
import random
import string

from django.shortcuts import render
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.reverse import reverse_lazy
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponseRedirect
from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule
from rest_framework.authtoken.models import Token

from notifications_app.repositories import NotificationRepository
from parser_app.models import UserPeriodicTasksModel
from parser_app.repositories import ParserRepository
from parser_app.utils import Parser


class Test(APIView):

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


class StartParser(APIView):

    def post(self, request):
        targets = ParserRepository(request.user).get_active_targets_list()
        Parser(request.user).start_parser(targets)
        NotificationRepository(request.user).create_notification(f"Проверка выполнена!")
        return JsonResponse({"status": "OK"}, status=200)


class ToggleTarget(APIView):

    def get(self, request, **kwargs):
        ParserRepository(request.user).toggle_target(kwargs.get('pk'))
        return HttpResponseRedirect(reverse_lazy('main:targets:list'))


class RemoveTarget(APIView):

    def get(self, request, **kwargs):
        ParserRepository(request.user).remove_target(kwargs.get('pk'))
        return HttpResponseRedirect(reverse_lazy('main:targets:list'))


class CreatePeriod(APIView):

    def post(self, request):
        title = ''.join(random.choice(string.ascii_letters) for _ in range(20))
        _time = request.data.get('time').split(':')
        hour = _time[0]
        minute = _time[1]
        task = PeriodicTask.objects.create(
            name=title,
            task="parser_start",
            crontab=CrontabSchedule.objects.get_or_create(hour=hour, minute=minute)[0],
            # interval=IntervalSchedule.objects.get_or_create(every=10, period='seconds')[0],
            kwargs=json.dumps({"user_id": request.user.id}),
            start_time=timezone.now(),
        )
        UserPeriodicTasksModel.objects.create(
            user=request.user,
            task=task
        )
        return HttpResponseRedirect(reverse_lazy('main:settings'))


class RemovePeriod(APIView):

    def get(self, request, **kwargs):
        try:
            UserPeriodicTasksModel.objects.get(pk=kwargs.get('pk')).task.delete()
        except UserPeriodicTasksModel.DoesNotExist:
            pass
        return HttpResponseRedirect(reverse_lazy('main:settings'))
