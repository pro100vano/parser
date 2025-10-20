
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework.views import APIView

from notifications_app.repositories import NotificationRepository, TgNotificationsRepository


class Notification(APIView):

    def post(self, request):
        NotificationRepository.create_notifications_for_all_users(request.data.get('message'))
        return JsonResponse({"detail": "OK"}, status=200)


class NotificationTg(APIView):

    def post(self, request):
        TgNotificationsRepository().asend_message_all(request.data.get('message'))
        return JsonResponse({"detail": "OK"}, status=200)


class Notifications(APIView):

    def get(self, request):
        context = dict()
        context['notifications'] = NotificationRepository(request.user).get_all()
        return render(
            request=request,
            template_name='list.html',
            context=context
        )


class ReadNotification(APIView):

    def post(self, request, **kwargs):
        notifications_repository = NotificationRepository(request.user)
        if notifications_repository.read(kwargs.get('pk', None)):
            nts = notifications_repository.get_unread_count()
            return JsonResponse({'detail': nts}, status=200)
        else:
            return JsonResponse({'detail': "ERR"}, status=400)


class TgUserAdd(APIView):

    def post(self, request):
        TgNotificationsRepository(request.user).add_user(request.data.get('tg_id'))
        return HttpResponseRedirect(reverse_lazy('main:settings'))


class TgUserRemove(APIView):

    def get(self, request, **kwargs):
        TgNotificationsRepository(request.user).remove_user(kwargs.get('pk'))
        return HttpResponseRedirect(reverse_lazy('main:settings'))

