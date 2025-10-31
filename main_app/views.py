import json

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from rest_framework.reverse import reverse_lazy
from rest_framework.views import APIView

from notifications_app.repositories import TgNotificationsRepository
from parser_app.models import UserPeriodicTasksModel
from parser_app.repositories import ParserRepository
from parser_app.utils import Parser


class Dashboard(APIView):

    def get(self, request):
        context = dict()
        context['targets_count'] = ParserRepository(request.user).get_targets_list_count()
        context['active_targets_count'] = ParserRepository(request.user).get_active_targets_list_count()
        return render(
            request=request,
            template_name='dashboard.html',
            context=context
        )


class TargetsList(APIView):

    def get(self, request):
        context = dict()
        context['targets'] = ParserRepository(request.user).get_targets_list()
        return render(
            request=request,
            template_name='targets/list.html',
            context=context
        )


class CreateTarget(APIView):

    def get(self, request):
        context = dict()
        context['types'] = ParserRepository.get_types()
        context['checking_types'] = ParserRepository.get_checking_types()
        return render(
            request=request,
            template_name='targets/create.html',
            context=context
        )

    def post(self, request):
        settings = request.data.get('params', None)
        settings = json.loads(settings) if settings is not None else None
        ParserRepository(request.user).create_target(
            title=request.data.get('title', None),
            url=request.data.get('link', None),
            target_type=request.data.get('type', None),
            params=settings
        )
        return JsonResponse({'detail': "OK", "redirect_to": reverse_lazy('main:targets:list')}, status=200)


class EditTarget(APIView):

    def get(self, request, **kwargs):
        context = dict()
        target = ParserRepository(request.user).get_target(kwargs.get('pk'))
        if target is None:
            return HttpResponseRedirect(reverse_lazy('main:targets:list'))
        context['target'] = target
        context['types'] = ParserRepository.get_types()
        context['checking_types'] = ParserRepository.get_checking_types()
        return render(
            request=request,
            template_name='targets/edit.html',
            context=context
        )

    def post(self, request, **kwargs):

        settings = request.data.get('params', None)
        settings = json.loads(settings) if settings is not None else None
        ParserRepository(request.user).edit_target(
            pk=kwargs.get('pk'),
            title=request.data.get('title', None),
            url=request.data.get('link', None),
            target_type=request.data.get('type', None),
            params=settings
        )
        return JsonResponse({'detail': "OK", "redirect_to": reverse_lazy('main:targets:list')}, status=200)


class StartTarget(APIView):

    def get(self, request, **kwargs):
        target = ParserRepository(request.user).get_target(pk=kwargs.get('pk'))
        Parser(request.user).test_parser(target)
        return HttpResponseRedirect(reverse_lazy('main:targets:list'))


class Reminder(APIView):

    def get(self, request):
        pass


class Settings(APIView):

    def get(self, request):
        context = dict()
        context['tg_code'] = TgNotificationsRepository(request.user).get_code()
        context['tg_users'] = TgNotificationsRepository(request.user).get_list()
        context['tasks'] = UserPeriodicTasksModel.objects.filter(user=request.user)
        return render(
            request=request,
            template_name='settings.html',
            context=context
        )


class Documentation(APIView):

    def get(self, request):
        return render(
            request=request,
            template_name='documentation.html'
        )


class TgHooks(APIView):

    def post(self, request):
        command = request.data.get('message').get('text')
        if command == '/start':
            TgNotificationsRepository().command_start(request.data)
        if command.startswith('/con'):
            TgNotificationsRepository().command_con(request.data)
        if command == '/list':
            TgNotificationsRepository().command_list(request.data)

        return JsonResponse({"detail": "OK"}, status=200)
