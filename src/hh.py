import time
import requests


class HeadHunter:

    def __init__(self, employer_id: str):
        self.employer_id = employer_id
        self.params = {'User-Agent': 'Mozilla/4.0', 'employer_id': self.employer_id, 'page': 0, 'per_pages': 100, 'archive': False}

    def get_request(self):
        """Функция возвращающая объект requests"""
        response = requests.get('https://api.hh.ru/vacancies', params=self.params)
        if response.status_code == 200:
            return response.json()

    @staticmethod
    def get_content(vacancy: dict):
        """Функция возвращающая кортеж данных по одной вакансии"""
        correct_salary = None
        currency = 'RUR'
        vacancy_id = int(vacancy.get('id'))
        title = vacancy.get('name')
        employer_id = int(vacancy.get('employer').get('id'))
        expierince = vacancy.get('experience').get('name')
        employment = vacancy.get('employment').get('name')
        requirement = vacancy.get('snippet').get('requirement')
        salary = vacancy.get('salary')
        url = vacancy.get('alternate_url')
        if salary and salary.get('currency') == 'RUR':
            correct_salary = salary.get('from') if salary.get('from') else salary.get('to')
            currency = salary.get('currency')
        vacancy_for_save = (
            vacancy_id, title, employer_id, expierince, employment, requirement, correct_salary, currency, url)
        return vacancy_for_save

    def get_vacancies(self):
        """Функция добавляющая в список кортежи с данными по одной вакансии"""
        all_vacancies = []
        cur_page = 0
        while True:
            self.params['page'] = cur_page
            result = self.get_request()
            if result is None:
                continue
            for item in result.get('items'):
                all_vacancies.append(self.get_content(item))
            cur_page += 1
            if cur_page > 5:
                break
            time.sleep(0.2)

        return all_vacancies
