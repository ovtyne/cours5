import math
import requests

from src.vacancy import Vacancy


class HeadHunterAPI:
    def get_request(self, keywords, page=0):
        """подключается к API и получает вакансии с применением фильтра"""
        url = "https://api.hh.ru/vacancies"

        params = {
            'area': 1,  # Поиск ощуществляется по вакансиям города Москва
            'page': page,  # Индекс страницы поиска на HH
            'per_page': 100,  # Кол-во вакансий на 1 странице
            'archive': False,
            'text': f'{keywords}'
        }

        response = requests.get(url, params).json()  # Посылаем запрос к API
        return response

    def get_vacancies(self, keywords, vac_n=100):
        """олучает вакансии, оставляет только нужные данные и возвращает список вакансий"""
        pages = math.ceil(vac_n / 100)
        v = {}

        for page in range(pages):
            request = self.get_request(keywords, page=page)
            if len(request['items']):
                v.update(request)

        vacancies = []

        if not len(v['items']):
            return vacancies

        for d in range(len(v)):
            pay = v['items'][d]['salary']

            if pay is None:
                pay_from = 0
                pay_to = 0
            else:
                pay_from = 0 if pay['from'] is None else pay['from']
                pay_to = 0 if pay['to'] is None else pay['to']

            vacancy = Vacancy(
                v['items'][d]['name'],
                v['items'][d]['alternate_url'],
                pay_from,
                pay_to,
                '',
                'HH'
            )
            vacancies.append(vacancy)

        return vacancies
