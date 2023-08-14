class Vacancy:
    """класс для работы с вакансиями"""

    def __init__(self, title, url, payment_from, payment_to, description, platform=""):
        """магический метод инициализации объекта"""
        self.title = title  #
        self.url = url
        self.payment_from = payment_from
        self.payment_to = payment_to
        self.description = description
        self.platform = platform  # hh или sj

    def __eq__(self, other):
        return (self.payment_from, self.payment_to) == (other.payment_from, other.payment_to)

    def __lt__(self, other):
        if not other.payment_from:
            return False
        if not self.payment_from:
            return True
        return self.payment_from < other.payment_from

    def __str__(self):
        """магический метод вывода информации о вакансии на экран"""
        title = ""
        description = ""
        url = ""
        payment = ""

        if self.title:
            title = f"{self.title}\n"
        if self.description:
            description = f"{self.description}\n"
        if self.payment_to == 0 and self.payment_from == 0:
            payment = "Оплата не указана\n"
        else:
            if isinstance(self.payment_from, int) and self.payment_from > 0:
                payment = f"от {self.payment_from} "
            if isinstance(self.payment_to, int) and self.payment_to > 0:
                payment += f"до {self.payment_to}"
            payment += " руб.\n"
        if self.url:
            url = f"адрес: {self.url}"
        vac_str = f"\n{title}{description}{payment}{url}\n---"
        return vac_str

    @staticmethod
    def print_top_vacancies(vacs, top_n=5):
        """Возвращает top_n первых из списка"""
        Vacancies.print_vacancies(vacs[:top_n])

    @staticmethod
    def print_vacancies(vacancies):
        """Выводит на экран все вакансии из списка"""
        for vacancy in vacancies:
            print(vacancy)

    @staticmethod
    def sort_vacancies_by_payment(vacancies, descend=True):
        """ Сортировка вакансий по убыванию зарплат"""
        return sorted(vacancies, reverse=descend)