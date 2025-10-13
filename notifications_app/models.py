from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class NotificationModel(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, null=False, blank=False)
    message = models.TextField(verbose_name="Сообщение")
    has_seen = models.BooleanField(verbose_name="Прочитано", default=False)
    date_created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"

    def draw_date(self):
        return timezone.localtime(self.date_created).strftime("%H:%M %d.%m")


class TgAccounts(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, null=False, blank=False)
    tg_id = models.CharField(max_length=100, verbose_name="id Телеграм")

    def __str__(self):
        return f"id: {self.tg_id}"

    class Meta:
        verbose_name = "Телеграм аккаут"
        verbose_name_plural = "Телеграм аккауты"
