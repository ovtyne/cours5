import psycopg2

from src.config import config


class DBManager:
    def __init__(self):
        self.name_db = 'vacancies_db'
        self.params = config()

    def create_database(self):
        """Метод создания базы данных и двух таблиц"""
        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True

        with conn.cursor() as cur:
            cur.execute(f"""DROP DATABASE IF EXISTS {self.name_db}""")
            cur.execute(f"""CREATE DATABASE {self.name_db}""")

        with psycopg2.connect(dbname=self.name_db, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""CREATE TABLE IF NOT EXISTS employers (
                    employer_id INT PRIMARY KEY,
                    company_name VARCHAR(50) UNIQUE NOT NULL);
                """)

                cur.execute(f"""CREATE TABLE IF NOT EXISTS vacancies (
                    vacancy_id INT PRIMARY KEY,
                    title VARCHAR(255),
                    employer_id INT REFERENCES employers(employer_id) NOT NULL,
                    expierence VARCHAR(255),
                    employment VARCHAR(255),
                    description VARCHAR(255),
                    salary INT,
                    currency VARCHAR(10),
                    url VARCHAR(30)
                    );
                """)

    def get_companies_and_vacancies_count(self):
        """Метод получает список всех компаний и количество вакансий у каждой компании."""
        with psycopg2.connect(dbname=self.name_db, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""SELECT company_name, COUNT(vacancy_id) FROM employers
                                INNER JOIN vacancies using(employer_id)
                                GROUP BY company_name""")
                rows = cur.fetchall()
                for row in rows:
                    print(f'Компания: {row[0]}, Количество вакансий: {row[1]}')

    def get_all_vacancies(self):
        """Метод получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки
        на вакансию"""
        with psycopg2.connect(dbname=self.name_db, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""SELECT company_name, title, salary, url
                                FROM vacancies
                                INNER JOIN employers USING(employer_id)""")
                rows = cur.fetchall()
                for row in rows:
                    print(f'Компания: {row[0]}, Наименование вакансии: {row[1]}, З.П.: {row[2]}, url: {row[3]}')

    def get_avg_salary(self):
        """метод получает среднюю зарплату по вакансиям"""
        with psycopg2.connect(dbname=self.name_db, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""SELECT AVG(salary)
                                FROM vacancies""")
                row = cur.fetchone()

                print(f'Средняя зароботная плата всех имеющихся вакансий: {round(row[0], 2)} руб')

    def get_vacancies_with_higher_salary(self):
        """Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        with psycopg2.connect(dbname=self.name_db, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT * FROM vacancies
                               WHERE salary > (SELECT AVG(salary) FROM vacancies)""")
                rows = cur.fetchall()
                print('Вакансии с зарплатой выше среднего')
                for row in rows:
                    print(row)

    def get_vacancies_with_keyword(self, word):
        """"Метод получает список всех вакансий, в названии которых слово"""
        with psycopg2.connect(dbname=self.name_db, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""SELECT * FROM vacancies
                                WHERE title like '%{word}%'""")
                rows = cur.fetchall()
                for row in rows:
                    print(row)

    def insert_to_employers(self, data: list):
        """Метод внесения данных в таблицу employers"""
        with psycopg2.connect(dbname=self.name_db, **self.params) as conn:
            with conn.cursor() as cur:
                cur.executemany(f"""INSERT INTO employers (employer_id, company_name)
                                VALUES(%s, %s)""", data)

    def insert_to_vacancies(self, data: list):
        """Метод внесения данных в таблицу vacancies"""
        with psycopg2.connect(dbname=self.name_db, **self.params) as conn:
            with conn.cursor() as cur:

                cur.executemany(f"""INSERT INTO vacancies (vacancy_id, title, employer_id, expierence, employment, description, salary, currency, url)
                                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (vacancy_id) DO NOTHING""",
                                data)



