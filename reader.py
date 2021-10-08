import csv
import json
import xml.etree.ElementTree as ET
import os


def read(filenames):
    res = {'n': 0}
    if len(filenames) == 0:
        print("В директории нет файлов с подходящим расширением")
        return {}
    for i in filenames:
        if i[-4:] == '.csv':  # Читаем csv
            res = read_csv(res, i, res['n'])
            print(i, 'прочитан')
        elif i[-5:] == '.json':  # Читаем json
            res = read_json(res, i, res['n'])
            print(i, 'прочитан')
        elif i[-4:] == '.xml':  # Читаем xml
            res = read_xml(res, i, res['n'])
            print(i, 'прочитан')
        if res == {}:
            return res
    return res


def read_csv(res, filename, n):
    b = False
    with open(filename) as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            if not b:  # Если на вход поступили заголовки
                l = len(row)
                # Для упорядочевания столбцов:
                key1 = [int(i[1:]) - 1 if i[0] == 'D' else -1 for i in row]
                key2 = [int(i[1:]) - 1 if i[0] == 'M' else -1 for i in row]
                b = True
                if res['n'] == 0:  # Вычисление n
                    res['n'] = len(list(filter(lambda x: x > -1, key1)))
                    n = res['n']
                continue
            # Группирую столбцы D i-ые
            arg = ' '.join(row[key1.index(i)] for i in range(n))
            if arg == '':
                print('Столбцы D отсутствуют, некорректный ввод данных.')
                return {}
            try:
                if arg in res.keys():  # Либо изменяем значения,
                    for i in range(n):
                        res[arg][i] += int(row[key2.index(i)])
                else:  # либо добавляем новый ключ
                    res[arg] = [int(row[key2.index(i)]) for i in range(n)]
            except ValueError:
                print(f'Значение столбца М в строке {arg}',
                       ' не является числом')
                return {}
            except IndexError:
                print('Количество столбцов M меньше значения n,',
                       ' некорректный ввод данных.')
                return {}
    return res


def read_json(res, filename, n):
    with open(filename) as file:
        input_value = json.load(file)
        first = input_value['fields'][0].keys()
        if res['n'] == 0:
            for i in first:
                if i[0] == 'D':
                    res['n'] += 1
            n = res['n']
        key1 = ['D' + str(i) for i in range(1, n+1)]
        key2 = ['M' + str(i) for i in range(1, n+1)]
        try:
            for row in input_value['fields']:
                arg = ' '.join(row[i] for i in key1)
                if arg in res.keys():
                    for i in range(n):
                        res[arg][i] += int(row[key2[i]])
                else:
                    res[arg] = [int(row[key2[i]]) for i in range(n)]
        except KeyError:
            print("Отсутвствует значение в столбце М или D")
            return{}
        except ValueError:
            print(f'Значение столбца М в строке {arg}',
                       ' не является числом')
            return {}
        except IndexError:
                print('Количество столбцов M меньше значения n,',
                       ' некорректный ввод данных.')
                return {}
    return res


def read_xml(res, filename, n):
    arg = ''
    tree = ET.parse(filename)  # Создаем дерево
    root = tree.getroot()  # Запоминаем корень
    b = True
    for one in root:  # Перебираем вершины
        row = {}
        for two in one:
            row[two.attrib['name']] = two[0].text
        if b:
            first = row.keys()
            if n == 0:
                for i in first:
                    if i[0] == 'D':
                        res['n'] += 1
                n = res['n']
            key1 = ['D' + str(i) for i in range(1, n+1)]
            key2 = ['M' + str(i) for i in range(1, n+1)]
            b = False
        try:
            arg = ' '.join(row[i] for i in key1)
            if arg in res.keys():
                for i in range(n):
                    res[arg][i] += int(row[key2[i]])
            else:
                res[arg] = [int(row[key2[i]]) for i in range(n)]
        except KeyError:
            print("Отсутвствует значение в столбце М или D")
            return{}
        except ValueError:
            print(f'Значение столбца М в строке {arg}',
                       ' не является числом')
            return {}
        except IndexError:
                print('Количество столбцов M меньше значения n,',
                       ' некорректный ввод данных.')
                return {}
    return res
