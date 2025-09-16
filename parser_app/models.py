from django.db import models


class TargetsModel(models.Model):
    title = models.CharField(max_length=100, verbose_name="Наименование")
    url = models.TextField(verbose_name="Ссылка")

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

    def __str__(self):
        return f"Настройка для {self.target.title}"

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайтов"
