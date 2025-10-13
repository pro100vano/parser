from django.db import models
from django.contrib.auth.models import User


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

    SIMPLE = 0
    DIFFICULT = 1
    AVITO = 2
    YANDEX = 3
    CIAN = 4
    TARGET_TYPE = (
        (SIMPLE, "Простая"),
        (DIFFICULT, "Сложная"),
        (AVITO, "Авито"),
        (YANDEX, "Яндекс"),
        (CIAN, "Циан"),
    )

    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='parser_owner', on_delete=models.CASCADE,
                             blank=False, null=False)
    title = models.CharField(max_length=100, verbose_name="Наименование")
    url = models.TextField(verbose_name="Ссылка")
    type = models.SmallIntegerField(verbose_name='Тип', choices=TARGET_TYPE, default=0)
    status = models.SmallIntegerField(verbose_name="Статус", choices=TARGET_STATUS, default=0)
    status_changed = models.DateTimeField(verbose_name="Статус изменился", default=None, null=True)
    activate = models.BooleanField(verbose_name="Активировать", default=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Сайт"
        verbose_name_plural = "Сайты"

    @property
    def short_url(self):
        if self.url.__len__() > 40:
            return f"{self.url[:40]}..."
        else:
            return self.url

    @property
    def target_settings(self):
        settings = []
        for setting in self.settings.all():
            settings.append(f"{setting.get_type_display()} {setting.type_param} ({setting.block})")
        return settings


class TargetSettingsModel(models.Model):

    NOT_EMPTY = 0
    LESS_ENTRIES = 1
    MORE_ENTRIES = 2
    CONTAINS = 3
    STARTS = 4
    ENDS = 5

    CHECKING_TYPE = (
        (NOT_EMPTY, 'Блок не пустой'),
        (LESS_ENTRIES, 'Элементов меньше чем'),
        (MORE_ENTRIES, 'Элементов больше чем'),
        (CONTAINS, 'Содержит'),
        (STARTS, 'Начинается с'),
        (ENDS, 'Заканчивается'),
    )

    target = models.ForeignKey(TargetsModel, verbose_name="Цель", related_name="settings", null=False, blank=False,
                               on_delete=models.CASCADE)
    type = models.SmallIntegerField(verbose_name='Тип', choices=CHECKING_TYPE, default=0)
    type_param = models.CharField(max_length=255, verbose_name="Дополнительный параметр", blank=True)
    block = models.TextField(verbose_name="Проверяемый блок", default='')

    def __str__(self):
        return f"Настройка для {self.target.title}"

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайтов"
