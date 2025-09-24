from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from tasks.sample_tasks import create_task


class Notification(APIView):

    def post(self, request):
        task_id = 1
        task = create_task.delay(task_id)
        return JsonResponse({"task_id": task.id}, status=202)
