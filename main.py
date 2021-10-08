import os
import csv
import reader
files = os.listdir()  # Взяли список файлов директории
res = reader.read(files)  # Транслировали информацию в словарь
key = sorted(res.keys())
if res == {}:
    Empty_file = open("result.tsv", "w+")
    Empty_file.write("ERROR")
    Empty_file.close()
else:
    with open('result.tsv', 'wt') as result:
        tsv_writer = csv.writer(result, delimiter='\t')
        # Печатаем заголовки:
        tsv_writer.writerow(['D' + str(i) for i in range(1, res['n']+1)] +
                            ['MS' + str(i) for i in range(1, res['n']+1)])
        # Заполняем файл данными
        for i in key[:-1]:
            tsv_writer.writerow(i.split() + res[i])
