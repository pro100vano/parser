import json

from django.shortcuts import render
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.reverse import reverse_lazy
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponseRedirect
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from rest_framework.authtoken.models import Token

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
    permission_classes = (AllowAny, )

    def post(self, request):
        user = Token.objects.get(key=request.headers.get('Authorization')).user
        targets = ParserRepository(user).get_active_targets_list()
        Parser(user).start_parser(targets)
        return JsonResponse({"status": "OK"}, status=200)


class ToggleTarget(APIView):

    def get(self, request, **kwargs):
        ParserRepository(request.user).toggle_target(kwargs.get('pk'))
        return HttpResponseRedirect(reverse_lazy('main:targets:list'))


class RemoveTarget(APIView):

    def get(self, request, **kwargs):
        ParserRepository(request.user).remove_target(kwargs.get('pk'))
        return HttpResponseRedirect(reverse_lazy('main:targets:list'))

