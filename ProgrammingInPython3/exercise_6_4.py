#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 4. Implement an Account class that holds an account number, an account
#    name, and a list of Transactions. The number should be a read-only prop-
#    erty; the name should be a read-write property with an assertion to ensure
#    that the name is at least four characters long. The class should support
#    the built-in len() function (returning the number of transactions), and
#    should provide two calculated read-only properties: balance which should
#    return the account’s balance in USD and all_usd which should return
#    True if all the transactions are in USD and False otherwise. Three other
#    methods should be provided: apply() to apply (add) a transaction, save(),
#    and load(). The save() and load() methods should use a binary pickle
#    with the filename being the account number with extension .acc; they
#    should save and load the account number, the name, and all the transactions.
#    This class can be implemented in about ninety lines with some
#    simple doctests that include saving and loading—use code such as name
#    = os.path.join(tempfile.gettempdir(), account_name) to provide a suitable
#    temporary filename, and make sure you delete the temporary file after the
#    tests have finished. A model solution is in file Account.py.

import pickle
from exercise_6_3 import Transaction


class Account(object):
    """
    Класс Account, хранит номер счёта, название счёта и список транзакций (объектов класса Transaction).
    >>> import os
    >>> import tempfile
    >>> name = os.path.join(tempfile.gettempdir(), "account1")
    >>> account = Account(name, "Huginn")
    >>> os.path.basename(account.number), account.name,
    ('account1', 'Huginn')
    >>> account.balance, account.all_usd, len(account)
    (0.0, True, 0)
    >>> account.apply(Transaction(100, "2018-12-30"))
    >>> account.apply(Transaction(200, "2018-12-31"))
    >>> account.apply(Transaction(-50, "2019-01-01"))
    >>> account.balance, account.all_usd, len(account)
    (250.0, True, 3)
    >>> account.apply(Transaction(50, "2019-01-01", "RUR", 0.015))
    >>> account.balance, account.all_usd, len(account)
    (250.75, False, 4)
    >>> account.save()
    >>> newaccount = Account(name, "Muninn")
    >>> newaccount.balance, newaccount.all_usd, len(newaccount)
    (0.0, True, 0)
    >>> newaccount.load()
    >>> newaccount.balance, newaccount.all_usd, len(newaccount)
    (250.75, False, 4)
    >>> try:
    ...     os.remove(name + ".acc")
    ... except EnvironmentError:
    ...     pass
    """

    def __init__(self, number, name):
        self.__number = number          # Номер счёта
        if not len(name) > 3:           # Проверка длины названия счёта
            raise AssertionError('Название счёта должно содержать не менее четырёх символов.')
        else:
            self.__name = name          # Название счёта
        self.__transactions = []        # Список транзакций (объектов класса Transaction)

    @property
    def number(self):
        """Номер счёта в виде свойства, доступного только для чтения."""
        return self.__number

    @property
    def name(self):
        """Название счёта в виде свойства, доступного для чтения."""
        return self.__name

    @name.setter
    def name(self, name):
        """Название счёта в виде свойства, доступного для записи."""
        return self.__name

    @property
    def balance(self):
        """Вычисляемое свойство, доступное только для чтения, возвращающее баланс счёта в долларах США."""
        balance = 0.0
        for transaction in self.__transactions:
            balance += transaction.usd
        return balance

    @property
    def all_usd(self):
        """Вычисляемое свойство, доступное только для чтения, возвращающее True,
        если все транзакции выполнялись в долларах США, или False - в противном случае."""
        for transaction in self.__transactions:
            if transaction.currency != "USD":
                return False
        return True

    def __len__(self):
        """Встроенная функция, возвращающая число транзакций."""
        return len(self.__transactions)

    def apply(self, transaction):
        """Функция реализующая метод для добавления транзакции."""
        self.__transactions.append(transaction)

    def save(self):
        """Функция реализующая метод сохранения объектов в двоичном формате, в файл,
        имя которого совпадает с номером счёта и с расширением .acc.
        Функция сохраняет номер счёта, название счёта и все транзакции."""
        fh = None
        try:
            data = [self.number, self.name, self.__transactions]
            fh = open(self.number + ".acc", "wb")
            pickle.dump(data, fh, pickle.HIGHEST_PROTOCOL)
        except (EnvironmentError, pickle.PicklingError) as err:
            raise print(str(err))
        finally:
            if fh is not None:
                fh.close()

    def load(self):
        """Функция реализующая метод загрузки объектов в двоичном формате, из файла,
        имя которого совпадает с номером счёта и с расширением .acc.
        Функция загружает номер счёта, название счёта и все транзакции."""
        fh = None
        try:
            fh = open(self.number + ".acc", "rb")
            data = pickle.load(fh)
            assert self.number == data[0], "account number doesn't match"
            self.__name, self.__transactions = data[1:]
        except (EnvironmentError, pickle.UnpicklingError) as err:
            raise print(str(err))
        finally:
            if fh is not None:
                fh.close()


if __name__ == "__main__":
    import os
    import tempfile
    name = os.path.join(tempfile.gettempdir(), "account1")
    account = Account(name, "Huginn")
    print('account number:', os.path.basename(account.number), '\naccount name:', account.name)
    print(account.balance, account.all_usd, len(account))
    account.apply(Transaction(100, "2018-12-30"))
    account.apply(Transaction(200, "2018-12-31"))
    account.apply(Transaction(-50, "2019-01-01"))
    print(account.balance, account.all_usd, len(account))
    account.apply(Transaction(50, "2019-01-01", "RUR", 0.015))
    print(account.balance, account.all_usd, len(account))
    print("Saving...")
    account.save()
    newaccount = Account(name, "Muninn")
    print('account number:', os.path.basename(newaccount.number), '\nnew account name:', newaccount.name)
    print(newaccount.balance, newaccount.all_usd, len(newaccount))
    print("Loading...")
    newaccount.load()
    print(newaccount.balance, newaccount.all_usd, len(newaccount))
    try:
        os.remove(name + ".acc")
    except EnvironmentError:
        pass
