import pathlib

from src.hh import HeadHunter
from src.db_manager import DBManager
from src.utils import read_file

PATH_TO_JSON = pathlib.Path(pathlib.Path.cwd(), '', 'employers.json')


def main():
    db = DBManager()
    db.create_database()
    answer = input("Обновить базу? (д/н)")
    if answer.lower() in ['y', 'д']:
        print("Обновление базы данных. Ожидайте")
        employers = read_file(PATH_TO_JSON)
        db.insert_to_employers(employers)

        step = 100 / len(employers)
        counter = 0
        for i in range(len(employers)):
            print(f"Обновлено {counter}%")
            head_hunter = HeadHunter(employers[i][0]).get_vacancies()
            db.insert_to_vacancies(head_hunter)
            counter += step

        print("Обновление завершено")

    while True:
        print('\nЧего изволите?   :)')
        print(f"1. Получить список всех компаний и количество вакансий у каждой компании \n"
              f"2. Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки "
              f"на вакансию \n"
              f"3. Получить среднюю зарплату по вакансиям \n"
              f"4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям \n"
              f"5. получает список всех вакансий, в названии которых содержатся слово\n"
              f"0. Выход из программы")
        print()
        user_input = input('Ваш выбор: ')
        if user_input == '1':
            db.get_companies_and_vacancies_count()
        elif user_input == '2':
            db.get_all_vacancies()
        elif user_input == '3':
            db.get_avg_salary()
        elif user_input == '4':
            db.get_vacancies_with_higher_salary()
        elif user_input == '5':
            word_input = input('Введите слово: ')
            db.get_vacancies_with_keyword(word_input)
        elif user_input == '0':
            break


if __name__ == '__main__':
    main()
