"""
Написать функцию host_range_ping_tab(),
возможности которой основаны на функции из примера 2.
Но в данном случае результат должен быть итоговым по всем ip-адресам,
представленным в табличном формате (использовать модуль tabulate).
Таблица должна состоять из двух колонок и выглядеть примерно так:

Reachable
10.0.0.1
10.0.0.2

Unreachable
10.0.0.3
10.0.0.4

"""
from ipaddress import ip_address
from itertools import zip_longest

from tabulate import tabulate

import t01_host_ping
import t02_host_range_ping


def ask_user_for_start_and_end_ips():
    """ Получит от пользователя нужную информацию и вернет """
    start_ipv4, how_many_ip_check = ip_address('127.0.0.1'), 2

    is_error = True
    while is_error:
        try:
            from_ip = input(
                'Введите начальный IP адрес для проверки диапазона адресов на доступность:'
            )
            start_ipv4 = ip_address(from_ip)
            is_error = False
        except ValueError:
            print("Ошибка. IP адрес не корректен.")

    is_error = True
    while is_error:
        try:
            how_many_ip_check = int(input('Сколько адресов просерить:'))
            is_error = False
        except ValueError:
            print("Ошибка. Количество хостов должно быть целый числом.")

    end_ipv4 = start_ipv4 + how_many_ip_check

    return start_ipv4, end_ipv4


def host_range_ping_tab():
    """ Выведет результат по всем ip-адресам, в табличном формате"""
    start_ip, end_ip = ask_user_for_start_and_end_ips()
    t02_host_range_ping.host_range_ping(start_ip, end_ip)


if __name__ == "__main__":
    host_range_ping_tab()

    print(' Результаты '.center(69, '-'))

    headers = t01_host_ping.PingResults.dict.keys()
    table = list(
        zip_longest(
            t01_host_ping.PingResults.dict[t01_host_ping.Host.AVAILABLE],
            t01_host_ping.PingResults.dict[t01_host_ping.Host.NOT_AVAILABLE],
            fillvalue=''
        )
    )
    print(tabulate(table, headers, tablefmt="pretty"))
