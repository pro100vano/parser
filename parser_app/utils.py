import requests
from bs4 import BeautifulSoup as BSoup
from .models import TargetsModel, TargetSettingsModel
from .repositories import ParserRepository


class Parser:

    def __init__(self, user=None):
        if user is not None:
            self.user = user

    def start_parser(self, targets):
        for target in targets:
            if target.type == TargetsModel.DIFFICULT:
                self.difficult_parser(target)
            elif target.type == TargetsModel.AVITO:
                self.avito_parser(target)
            elif target.type == TargetsModel.YANDEX:
                self.yandex_parser(target)
            elif target.type == TargetsModel.CIAN:
                self.cian_parser(target)
            else:
                self.simple_parser(target)

    def simple_parser(self, target):
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(target.url, headers=headers)
        if response.status_code == 200:
            ParserRepository.change_status(target, TargetsModel.SUCCESS)
        else:
            ParserRepository.change_status(target, TargetsModel.ERROR)

    def avito_parser(self, target):
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(target.url, headers=headers)
        if response.status_code == 200:
            ParserRepository.change_status(target, TargetsModel.SUCCESS)
        else:
            ParserRepository.change_status(target, TargetsModel.ERROR)

    def yandex_parser(self, target):
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(target.url, headers=headers)
        if response.status_code == 200:
            ParserRepository.change_status(target, TargetsModel.SUCCESS)
        else:
            ParserRepository.change_status(target, TargetsModel.ERROR)

    def cian_parser(self, target):
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"}
        response = requests.get(target.url, headers=headers)
        if response.status_code == 200:
            ParserRepository.change_status(target, TargetsModel.SUCCESS)
        else:
            ParserRepository.change_status(target, TargetsModel.ERROR)

    def difficult_parser(self, target):
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"}
        response = requests.get(target.url, headers=headers)
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

            if success:
                ParserRepository.change_status(target, TargetsModel.SUCCESS)
            else:
                ParserRepository.change_status(target, TargetsModel.WARNING)
        else:
            ParserRepository.change_status(target, TargetsModel.ERROR)

    def soup_search(self, soup, searched):
        searched_list = searched.split(' ')
        cur_level = searched_list.pop(0)
        cur_class = cur_level.split('.')
        # cur_id = cur_level.split('#')
        # if cur_id.__len__() > 1:
        #     next_soup = soup.find(cur_id[0], id=cur_id[1])
        # elif cur_class.__len__() > 1:
        if cur_class.__len__() > 1:
            next_soup = soup.find(cur_class[0], class_=cur_class[1])
        else:
            next_soup = soup.find(cur_level)
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
        if [i for i in block.contents if i.name is not None].__len__() > 0:
            return True
        return False

    def parser_less_entries(self, html, setting):
        try:
            soup = BSoup(html, 'html.parser')
            block = self.soup_search(soup, setting.block)
        except Exception as e:
            print(e)
            return False
        if [i for i in block.contents if i.name is not None].__len__() < setting.type_param:
            return True
        return False

    def parser_more_entries(self, html, setting):
        try:
            soup = BSoup(html, 'html.parser')
            block = self.soup_search(soup, setting.block)
        except Exception as e:
            print(e)
            return False
        if [i for i in block.contents if i.name is not None].__len__() > setting.type_param:
            return True
        return False
