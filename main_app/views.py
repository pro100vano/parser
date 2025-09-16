from django.shortcuts import render
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


