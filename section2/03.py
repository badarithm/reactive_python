import csv
import os.path

from rx import Observable

def read_csv(filename: str) :
    with(open(filename)) as file:
        lines = file.readlines()
        csv_reader = csv.reader(lines[1:])
        return csv_reader

def row_to_dict(row):
    return {
        'id': int(row[0]),
        'filename': row[1],
        'lines': int(row[2]),
        'size' : int(row[3]),
    }

files = ['test.csv', 'test2.csv']

source = Observable.merge([Observable.from_iterable(read_csv(filename)) for filename in files]).map(row_to_dict)

published = source.publish()

def print_row(row):
    print('File "{filename}" has {lines} lines and is size is {size} kb'.format(**row))

def print_group(group):
    return group.subscribe(print_row)

maximum = published.max(lambda a, b: a['lines'] - b['lines'])
maximum.subscribe()