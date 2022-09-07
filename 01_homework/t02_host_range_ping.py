"""
Написать функцию host_range_ping() (возможности которой основаны на функции из примера 1)
для перебора ip-адресов из заданного диапазона.
Меняться должен только последний октет каждого адреса.
По результатам проверки должно выводиться соответствующее сообщение.
"""

from ipaddress import ip_address
from pprint import pprint

import t01_host_ping


def host_range_ping(from_ip: str, to_ip: str):
    """ Произведет перебор ip-адресов из заданного диапазона. """
    ipv4 = ip_address(from_ip)
    to_ipv4 = ip_address(to_ip) + 1
    ips_list = []
    stop_flag = False
    if ipv4 > to_ipv4:
        raise ValueError(
            'IP адрес, левой границы диапазона должен быть меньше IP адреса правой границы диапазона')

    while not stop_flag:
        if ipv4 != to_ipv4:
            # print(str(ipv4))
            ips_list.append(str(ipv4))
            ipv4 += 1
        else:
            stop_flag = True

    print(f'Сканируем {len(ips_list)} хостов:')

    t01_host_ping.host_ping(ips_list)


if __name__ == "__main__":
    FROM_IP = '8.8.8.0'
    TO_IP = '8.8.10.2'

    host_range_ping(FROM_IP, TO_IP)

    print(' Результаты '.center(69, '-'))
    pprint(t01_host_ping.PingResults.dict)
