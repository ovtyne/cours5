CREATE TABLE IF NOT EXISTS AVG_salary AS
                    SELECT AVG(vacancies.salary_max)
                    FROM vacancies;

CREATE TABLE IF NOT EXISTS higher_salary AS
                        SELECT vacancies.employer, vacancies.url, vacancies.salary_max, vacancies.name
                        FROM vacancies
                        WHERE vacancies.salary_max > (SELECT AVG(vacancies.salary_max)
                        FROM vacancies);

CREATE TABLE IF NOT EXISTS companies_and_vacancies_count AS
                    SELECT vacancies.employer, COUNT(vacancies.id)
                    FROM vacancies
                    GROUP BY vacancies.employer;

CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                url TEXT NOT NULL,
                salary_min INTEGER,
                salary_max INTEGER,
                employer TEXT NOT NULL
                );