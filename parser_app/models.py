from django.db import models


class TargetsModel(models.Model):
    CREATED = 0
    SUCCESS = 1
    ERROR = 2
    WARNING = 3
    TARGET_STATUS = (
        (CREATED, "--------"),
        (SUCCESS, "Успешно"),
        (ERROR, "Ошибка"),
        (WARNING, "Доступен")
    )

    title = models.CharField(max_length=100, verbose_name="Наименование")
    url = models.TextField(verbose_name="Ссылка")
    status = models.SmallIntegerField(verbose_name="Статус", choices=TARGET_STATUS, default=0)
    status_changed = models.DateTimeField(verbose_name="Статус изменился", default=None, null=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Сайт"
        verbose_name_plural = "Сайты"

    @property
    def short_url(self):
        if self.url.__len__() > 100:
            return f"{self.url[:100]}..."
        else:
            return self.url


class TargetSettingsModel(models.Model):
    target = models.ForeignKey(TargetsModel, verbose_name="Цель", related_name="settings", null=False, blank=False,
                               on_delete=models.CASCADE)
    message = models.TextField('Test')

    def __str__(self):
        return f"Настройка для {self.target.title}"

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайтов"
