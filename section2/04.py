from rx import Observable
from rx.testing import TestScheduler


def print_value(x):
    return print(x)

Observable.from_([1, 2, 3]).map(lambda x: x -1).subscribe(print_value)
Observable.from_([{'a': 1},{'b': 2},{'c': 3}]).map(lambda data: {**data, 'hello': 'world'}).subscribe(print_value)

print('-- Flat Map')
def read_lat_line_from_file(filename: str):
    with  open(filename) as file:
        lines = file.readlines()
        last_line = lines[-1]
        return Observable.just(last_line)

read_lat_line_from_file('test.csv').flat_map(lambda line: read_lat_line_from_file('test2.csv')).subscribe(print_value)

print('window') # window is like a buffer

print('window with count')

Observable.from_(range(3)).window_with_count(2).flat_map(lambda x: x).subscribe(print_value)

print('window with time')
test_scheduler = TestScheduler()

Observable.interval(50, test_scheduler).take_until(Observable.timer(100)).window_with_time(10).subscribe(
    lambda observable: observable.count().subscribe(print_value)
)
test_scheduler.start()
print('combine latest')
test_scheduler = TestScheduler()
Observable.combine_latest(
    Observable.interval(1, test_scheduler).map(lambda x: 'a {}'.format(x)),
    Observable.interval(2, test_scheduler).map(lambda x: 'b {}'.format(x)),
    lambda a, b, : '{} {}'.format(a, b)
).take_until(Observable.timer(5)).subscribe(print)

# test_scheduler.start()

print('-- zip')
# test_scheduler = TestScheduler()

Observable.combine_latest(
    Observable.interval(1, test_scheduler).map(lambda x: 'a {}'.format(x)),
    Observable.interval(2, test_scheduler).map(lambda x: 'b {}'.format(x)),
    lambda a, b, : '{} {}'.format(a, b)
).take_until(Observable.timer(5)).subscribe(print)
test_scheduler.start()
