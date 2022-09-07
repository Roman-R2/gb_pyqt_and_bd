"""
Написать функцию host_ping(), в которой с помощью утилиты ping будет
проверяться доступность сетевых узлов. Аргументом функции является список,
в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
В функции необходимо перебирать ip-адреса и проверять их доступность с выводом
соответствующего сообщения («Узел доступен», «Узел недоступен»).
При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().

(
Внимание! Аргументом сабпроцесcа должен быть список, а не строка!!!
Для уменьшения времени работы скрипта при проверке нескольких ip-адресов,
решение необходимо выполнить с помощью потоков
)

"""
import platform
import subprocess
import time
from ipaddress import ip_address
import threading
from pprint import pprint

SHARED_RESOURCE_LOCK = threading.Lock()


class Host:
    AVAILABLE = "Доступные"
    NOT_AVAILABLE = "Не доступные"


class PingResults:
    dict = {
        Host.AVAILABLE: [],
        Host.NOT_AVAILABLE: []
    }


def is_ip_address(value):
    """ Проверит, что введеное занчение это ip адрес. """
    try:
        ipv4 = ip_address(value)
    except ValueError:
        raise ValueError("Это не ip адрес.")
    return ipv4


def ping(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    response = subprocess.Popen(
        ['ping', param, '1', '-w', '2', str(host)],
        stdout=subprocess.PIPE
    )
    if response.wait() == 0:
        with SHARED_RESOURCE_LOCK:
            PingResults.dict[Host.AVAILABLE].append(str(host))
            result = f'{host}: {Host.AVAILABLE}'

    else:
        with SHARED_RESOURCE_LOCK:
            PingResults.dict[Host.NOT_AVAILABLE].append(str(host))
            result = f'{host}: {Host.NOT_AVAILABLE}'
    return result


def host_ping(hosts: list):
    """ Проверит доступность сетевых узлов. """
    treads = []
    for host in hosts:
        try:
            ipv4 = is_ip_address(host)
        except ValueError:
            ipv4 = host

        thread = threading.Thread(target=ping, args=(ipv4,), daemon=True)
        thread.start()
        treads.append(thread)

    for tread in treads:
        tread.join()


if __name__ == "__main__":
    hosts_for_ping = [
        '178.248.233.33', 'ya.ru', 'ipconfig.me', '8.8.8.8', '192.168.0.1',
        '0.0.0.1', '127.0.0.1'
    ]

    print(f'Сканируем {len(hosts_for_ping)} хостов:')
    start = time.time()
    host_ping(hosts_for_ping)
    end = time.time()

    print(' Результаты '.center(69, '-'))
    pprint(PingResults.dict)

    print(f'\nСкрипт отработал {end - start} секунд')
