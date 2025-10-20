import requests
import time
from asgiref.sync import async_to_sync
from bs4 import BeautifulSoup as BSoup

from notifications_app.repositories import NotificationRepository, TgNotificationsRepository
from .models import TargetsModel, TargetSettingsModel
from .repositories import ParserRepository


class Parser:
    timeout = 30

    def __init__(self, user=None):
        if user is not None:
            self.user = user

    def start_parser(self, targets):
        notification_message = ""
        for target in targets:
            start = time.perf_counter()
            try:
                if target.type == TargetsModel.DIFFICULT:
                    result = self.difficult_parser(target)
                elif target.type == TargetsModel.AVITO:
                    result = self.avito_parser(target)
                elif target.type == TargetsModel.YANDEX:
                    result = self.yandex_parser(target)
                elif target.type == TargetsModel.CIAN:
                    result = self.cian_parser(target)
                else:
                    result = self.simple_parser(target)
            except Exception as e:
                result = TargetsModel.ERROR
                print(e)
            load_time = time.perf_counter() - start
            ParserRepository.change_status(target, result)
            if result != TargetsModel.ERROR:
                if result == TargetsModel.SUCCESS:
                    notification_message += f"🟢\"{target.title}\" доступен. "
                else:
                    notification_message += f"🟠\"{target.title}\" доступен, но имеет ошибки. "
                notification_message += f"Отклик: {round(load_time, 3)} сек.\n"
            else:
                notification_message += f"🔴\"{target.title}\" не доступен\n"
                NotificationRepository(self.user).create_notification(f"\"{target.title}\" не доступен")
        async_to_sync(TgNotificationsRepository(self.user).asend_message_all)(notification_message)

    def simple_parser(self, target):
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(target.url, headers=headers, timeout=self.timeout)
        if response.status_code == 200:
            return TargetsModel.SUCCESS
        else:
            return TargetsModel.ERROR

    def avito_parser(self, target):
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(target.url, headers=headers, timeout=self.timeout)
        if response.status_code == 200:
            return TargetsModel.SUCCESS
        else:
            return TargetsModel.ERROR

    def yandex_parser(self, target):
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(target.url, headers=headers, timeout=self.timeout)
        if response.status_code == 200:
            return TargetsModel.SUCCESS
        else:
            return TargetsModel.ERROR

    def cian_parser(self, target):
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"}
        response = requests.get(target.url, headers=headers, timeout=self.timeout)
        if response.status_code == 200:
            return TargetsModel.SUCCESS
        else:
            return TargetsModel.ERROR

    def difficult_parser(self, target):
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"}
        response = requests.get(target.url, headers=headers, timeout=self.timeout)
        if response.status_code == 200:
            success = True
            for setting in target.settings.all():
                if setting.type == TargetSettingsModel.NOT_EMPTY:
                    if not self.parser_not_empty(response.text, setting):
                        success = False
                elif setting.type == TargetSettingsModel.LESS_ENTRIES:
                    if not self.parser_less_entries(response.text, setting):
                        success = False
                elif setting.type == TargetSettingsModel.MORE_ENTRIES:
                    if not self.parser_more_entries(response.text, setting):
                        success = False
                elif setting.type == TargetSettingsModel.CONTAINS:
                    if not self.parser_contains(response.text, setting):
                        success = False
                elif setting.type == TargetSettingsModel.STARTS:
                    if not self.parser_starts(response.text, setting):
                        success = False
                elif setting.type == TargetSettingsModel.ENDS:
                    if not self.parser_ends(response.text, setting):
                        success = False
            if success:
                return TargetsModel.SUCCESS
            else:
                return TargetsModel.WARNING
        else:
            return TargetsModel.ERROR

    def soup_search(self, soup, searched):
        searched_list = searched.split(' ')
        cur_level = searched_list.pop(0)
        cur_class = cur_level.split('.')
        if cur_class.__len__() > 1:
            cur_nums = cur_class[1].split(':')
            cur_num = cur_nums[1] if cur_nums.__len__() > 1 else None
            next_soup = soup.find_all(cur_class[0], class_=cur_nums[0])
        else:
            cur_nums = cur_level.split(':')
            cur_num = cur_nums[1] if cur_nums.__len__() > 1 else None
            next_soup = soup.find_all(cur_level)
        if cur_num is not None:
            next_soup = next_soup[int(cur_num)]
        else:
            next_soup = next_soup[0]
        if searched_list.__len__() < 1:
            return next_soup
        return self.soup_search(next_soup, ' '.join(searched_list))

    def parser_not_empty(self, html, setting):
        try:
            soup = BSoup(html, 'html.parser')
            block = self.soup_search(soup, setting.block)
        except Exception as e:
            print(e)
            return False
        contents = [i.name for i in block.contents if i.name is not None]
        if contents.__len__() > 0 and contents[0] == 'template':
            return False
        if contents.__len__() > 0:
            return True
        return False

    def parser_less_entries(self, html, setting):
        try:
            soup = BSoup(html, 'html.parser')
            block = self.soup_search(soup, setting.block)
        except Exception as e:
            print(e)
            return False
        contents = [i.name for i in block.contents if i.name is not None]
        if contents.__len__() > 0 and contents[0] == 'template':
            return False
        if contents.__len__() < setting.type_param:
            return True
        return False

    def parser_more_entries(self, html, setting):
        try:
            soup = BSoup(html, 'html.parser')
            block = self.soup_search(soup, setting.block)
        except Exception as e:
            print(e)
            return False
        contents = [i.name for i in block.contents if i.name is not None]
        if contents.__len__() > 0 and contents[0] == 'template':
            return False
        if contents.__len__() > setting.type_param:
            return True
        return False

    def parser_contains(self, html, setting):
        try:
            soup = BSoup(html, 'html.parser')
            block = self.soup_search(soup, setting.block)
            content = ''.join([str(i).strip() for i in block.contents])
        except Exception as e:
            print(e)
            return False
        if content.__contains__(setting.type_param):
            return True
        return False

    def parser_starts(self, html, setting):
        try:
            soup = BSoup(html, 'html.parser')
            block = self.soup_search(soup, setting.block)
            content = ''.join([str(i).strip() for i in block.contents])
        except Exception as e:
            print(e)
            return False
        if content.startswith(setting.type_param):
            return True
        return False

    def parser_ends(self, html, setting):
        try:
            soup = BSoup(html, 'html.parser')
            block = self.soup_search(soup, setting.block)
            content = ''.join([str(i).strip() for i in block.contents])
        except Exception as e:
            print(e)
            return False
        if content.endswith(setting.type_param):
            return True
        return False
