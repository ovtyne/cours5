import json
import requests


class ParsingError(Exception):
    def __str__(self):
        return 'Ошибка получения данных по API'


class Vacancy:
    """Класс вакансий"""
    __slots__ = ('id', 'title', 'url', 'salary_from', 'salary_to', 'employer', 'api')

    def __init__(self, vacancy_id, title, url, salary_from, salary_to, employer, api):
        self.id = vacancy_id
        self.title = title
        self.url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.employer = employer
        self.api = api

    def __gt__(self, other):
        """Сравнение вакансий по зарплате """
        if not other.salary_from:
            return True
        elif not self.salary_from:
            return False
        return self.salary_from >= other.salary_from

    def __str__(self):
        """ Проверка минимального порога и максимального потолка зарплат"""
        salary_from = f'От {self.salary_from}' if self.salary_from else ''
        salary_to = f'До {self.salary_to}' if self.salary_to else ''
        if self.salary_from is None and self.salary_to is None:
            salary_from = 'Не указана'
        return (f'Вакансия: \"{self.title}\" \nКомпания: \"{self.employer}\" \nЗарплата: {salary_from} '
                f'{salary_to} \nURL:{self.url}')


class HeadHunter:
    """ Класс  HeadHunter"""

    def __init__(self, keyword):
        self.__header = {
            "User-Agent": "Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion"}
        self.__params = {
            "text": keyword,
            "page": 0,
            "per_page": 100,
        }
        self.__vacancies = []

    @staticmethod
    def get_salary(salary):
        """ Изменение зарплат если в евро"""
        formatted_salary = [None, None]
        if salary and salary['from'] and salary['from'] != 0:
            formatted_salary[0] = salary['from'] if salary['currency'].lower() == 'rur' else salary['from'] * 80
        if salary and salary['to'] and salary['to'] != 0:
            formatted_salary[1] = salary['to'] if salary['currency'].lower() == 'rur' else salary['to'] * 80
        return formatted_salary

    def get_request(self):
        """ Создание запроса по API"""
        response = requests.get('https://api.hh.ru/vacancies',
                                headers=self.__header,
                                params=self.__params)
        if response.status_code != 200:
            raise ParsingError
        return response.json()['items']

    def get_formatted_vacancies(self):
        """Извлечение из вакансии необходимых полей """
        formatted_vacancies = []
        for vacancy in self.__vacancies:
            salary_from, salary_to = self.get_salary(vacancy['salary'])
            formatted_vacancies.append({
                'id': vacancy['id'],
                'title': vacancy['name'],
                'url': vacancy['alternate_url'],
                'salary_from': salary_from,
                'salary_to': salary_to,
                'employer': vacancy['employer']['name'],
                'api': 'HeadHunter',
            })
        return formatted_vacancies

    def get_vacancies(self, pages_count=1):
        """ Перебор вакансий в цикле согласно количеству переопределенных в main страниц"""
        print(f"Парсинг страниц HeadHunter")
        vac_count = 0
        while self.__params['page'] < pages_count:
            try:
                values = self.get_request()
            except ParsingError:
                print('Ошибка получения данных')
                break
            vac_count += len(values)
            self.__vacancies.extend(values)
            self.__params['page'] += 1

        print(f'Найдено {vac_count} вакансий.')


class Connector:
    """Создание класса для работы с json файлом с вакансиями"""

    def __init__(self, keyword, vacancies_json):
        self.__filename = f'{keyword.title()}.json'
        self.insert(vacancies_json)

    def insert(self, vacancies_json):
        """ Внесение данных о вакансиях в json файл """
        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump(vacancies_json, file, ensure_ascii=False, indent=4)

    def select(self):
        """ Извлечение из json файла данных о вакансии с заданными параметрами """
        with open(self.__filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        vacancies = [Vacancy(x['id'], x['title'], x['url'], x['salary_from'], x['salary_to'], x['employer'], x['api'])
                     for x in data]
        return vacancies
