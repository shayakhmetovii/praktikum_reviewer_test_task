import datetime as dt


class Record:
    # не хватает docstring, typehints
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    # не хватает docstring, typehints
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    # не хватает docstring, typehints
    def add_record(self, record):
        self.records.append(record)

    # не хватает docstring, typehints
    def get_today_stats(self):
        today_stats = 0
        # переменная должна быть в нижнем регистре т.е. record
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    # не хватает docstring, typehints
    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            """
            выражение можно упростить 0 <= ... < 7
            (today - record.date) лучше предварительно рассчитать и дальше подставлять результат через переменную
            """
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # не хватает docstring, typehints
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            # перенос лучше делать через скобки, лучше читаемость
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        # else тут можно не писать
        else:
            return('Хватит есть!')


class CashCalculator(Calculator):
    """
    не хватает typehints, если это константы лучше пометить их как typing.Final и вынести за пределы класса
    если это не константы, сменить регистр переменных в нижний
    чтобы обозначить float лучше использовать запись 60.0 70.0
    """
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.


    """
    не хватает docstring, typehints, убрать лишние аргументы USD_RATE/EURO_RATE,
    они уже доступны для методов класса CashCalculator
    лучше переносить каждый аргумент функции на отдельную строку и обрамлять запятыми
    это улучшит читаемость, поможет быстро добавить новые аргументы или разрешить конфликты при слиянии
    currency некорректно обрабатывается: нет обработки неизвесного типа, сравнение строк лучше производить после 
    приведения к общему регистру, например, lowercase
    """
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # ошибка, возможно, имелось ввиду присвоение (=), а не сравнение (==)
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # если изначально заложено, что функция может вернуть None, а не только str,
        # то лучше явно прописать в конце return None
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)


    # не хватает docstring, typehints, проброса результат род функции через return
    # без доп сведений непонятно, зачем нужно переопределение родительского метода
    def get_week_stats(self):
        super().get_week_stats()


"""
Общие рекомендации:
1. настроить линтеры, анализаторы: flake8/ruff, mypy
для проверки соответствия кода PEP8, типизации
2. корреткно оформить репозиторий: добавить .gitignore чтобы исключить попадания служебных/ненужных файлов, секретов,
добавить requirements
3. придерживаться единого стиля: либо юзать fстроки, либо .format
4. добавить unit тесты: это важная часть разработки, которая играет на долгую.
5. Коммиты в репозитории должны быть более информативными
"""