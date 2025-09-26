import json

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from rest_framework.reverse import reverse_lazy
from rest_framework.views import APIView

from parser_app.repositories import ParserRepository


class Dashboard(APIView):

    def get(self, request):
        return render(
            request=request,
            template_name='dashboard.html'
        )


class TargetsList(APIView):

    def get(self, request):
        context = dict()
        context['targets'] = ParserRepository.get_targets_list()
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
        ParserRepository.create_target(
            title=request.data.get('title', None),
            url=request.data.get('link', None),
            target_type=request.data.get('type', None),
            params=settings
        )
        return JsonResponse({'detail': "OK", "redirect_to": reverse_lazy('main:targets:list')}, status=200)


