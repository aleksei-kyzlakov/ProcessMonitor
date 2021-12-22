# Задача 1
# Написать программу, которая будет запускать процесс и с указанным интервалом
# времени собирать о нём следующую статистику:
# •	Загрузка CPU (в процентах);
# •	Потребление памяти: Working Set и Private Bytes (для Windows-систем) или
#   Resident Set Size и Virtual Memory Size (для Linux-систем);
# •	Количество открытых хендлов (для Windows-систем) или файловых дескрипторов
#   (для Linux-систем).
# Сбор статистики должен осуществляться всё время работы запущенного процесса.
# Путь к файлу, который необходимо запустить, и интервал сбора статистики
# должны указываться пользователем. Собранную статистику необходимо сохранить
# на диске. Представление данных должно в дальнейшем позволять использовать
# эту статистику для автоматизированного построения графиков потребления
# ресурсов.

import psutil
import time


def monitor(interval, process):
    # если в переменной число, отслеживаем запущенный процесс по PID
    if isinstance(process, int):
        print('Monitoring running process. Press ctrl-C to exit')
        try:
            pp = psutil.Process(process)
        except OSError:
            print('No such process')
            return
    # если в переменной строка, пробуем выполнить коммандную строку
    else:
        try:
            pp = psutil.Popen(process.split())
        except OSError:
            print('No such programm')
            return
    # пока процесс запущен собираем статистику через заданный интервал
    try:
        while pp.is_running():
            with pp.oneshot():
                report = {'timestamp': time.time_ns(), 'pid': pp.pid,
                          'name': pp.name(), 'num_handles': pp.num_handles(),
                          'cpu_percent': pp.cpu_percent(),
                          'working_set': pp.memory_info().rss,
                          'private_bytes': pp.memory_info().private}
                with open(f'{pp.pid}', 'a') as file:
                    file.write(f'{report}\n')
                print(report)
                time.sleep(interval)
    # выход по завершению процесса, либо прерыванием ctrl-c
    except (OSError, KeyboardInterrupt):
        print(f'Exiting. Process is {pp.status()}')


def get_process():
    # просим ввести коммандную строку, либо PID, либо ентер для теста
    while True:
        process = input('''Enter programm to start or running process
                        PID to monitor (default \"python test.py\"):''')
        if process == '':
            process = "python test.py"
        elif process.isdigit():
            process = int(process)
        return process


def get_interval():
    # просим ввести интервал, дробное > 0, либо ентер для 0.1 по умолчанию
    while True:
        interval = input('Enter interval to gather stats(default \"0.1\"):')
        if interval == '':
            return 0.1
        else:
            try:
                interval = float(interval)
            except ValueError:
                print('Incorrect input, try again')
                continue
            if interval >= 0:
                return interval
            else:
                print('Positive floating point number only')


def main():
    if psutil.WINDOWS is True:      # опреационная система Windows
        monitor(get_interval(), get_process())
    else:
        print('Need Windows OS')


if __name__ == "__main__":
    main()
