#!/usr/bin/env python3
# 3. Implement a Transaction class that takes an amount, a date, a currency
#    (default “USD”—U.S. dollars), a USD conversion rate (default 1),
#    and a description (default None). All of the data attributes must be private.
#    Provide the following read-only properties: amount, date, currency,
#    usd_conversion_rate, description, and usd (calculated from amount *
#    usd_conversion_rate). This class can be implemented in about sixty lines
#    including some simple doctests. A model solution for this exercise (and the
#    next one) is in file Account.py.


class Transaction:

    def __init__(self, amount, date, currency="USD",
                 usd_conversion_rate=1, description=None):
        """
        >>> t = Transaction(100, "2018-12-19")
        >>> t.amount, t.currency, t.usd_conversion_rate, t.usd
        (100, 'USD', 1, 100)
        >>> t = Transaction(100, "2018-12-19", "RUR", 0.015)
        >>> t.amount, t.currency, t.usd_conversion_rate, t.usd
        (100, 'RUR', 0.015, 1.5)
        """
        self.__amount = amount
        self.__date = date
        self.__description = description
        self.__currency = currency
        self.__usd_conversion_rate = usd_conversion_rate

    # @property конвертирует методы класса в атрибуты только для чтения,
    # позволяя обращаться к методам не как к функциям, а как к атрибутам
    @property
    def amount(self):
        return self.__amount

    @property
    def date(self):
        return self.__date

    @property
    def description(self):
        return self.__description

    @property
    def currency(self):
        return self.__currency

    @property
    def usd_conversion_rate(self):
        return self.__usd_conversion_rate

    @property
    def usd(self):
        return self.__amount * self.__usd_conversion_rate


if __name__ == "__main__":
    t = Transaction(100, "2018-12-19")
    print(t.amount, t.currency, t.usd_conversion_rate, t.usd)
    t = Transaction(100, "2018-12-19", "RUR", 0.015)
    print(t.amount, t.currency, t.usd_conversion_rate, t.usd)
