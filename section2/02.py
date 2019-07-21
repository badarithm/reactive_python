from rx import Observable
from typing import Callable
from rx.testing import marbles, TestScheduler
from random import randint
def print_value(value: str) -> None:
    print("{} is the value".format(value))

test_scheduler:TestScheduler = TestScheduler()


#
# Observable.from_(['abc', 'def', 'ghi']).subscribe(print_value)
#
# def say_hello(name: str, callback: Callable) -> None:
#     callback("Hello {}!".format(name))
#
# hello = Observable.from_callback(say_hello)
# hello('Rudolf').subscribe(print_value)
# hello('observable').subscribe(print_value)
#
# Observable.from_list([1, 2, 3, 4, 5, 6]).subscribe(print_value)
# Observable.of(1,2, 3, 4, 5, 6, 7, 'A', 'B', 'C').subscribe(print_value)
#
#
# Observable.from_marbles('--(a1)-(b2)---(c3)|', test_scheduler).subscribe(print_value)
# Observable.from_marbles('--(a6)---(b5)(c4)|', test_scheduler).subscribe(print_value)
#
#
# Observable.interval(10, test_scheduler).take_until(Observable.timer(30)).subscribe(print_value)
# print('-- Buffer')
# Observable.from_range(range(2000)).buffer(Observable.interval(1)).subscribe(lambda buffer:print('# of items in buffer : {}'.format(len(buffer))))
# print('-- Buffer with count')
# Observable.from_(range(10)).buffer_with_count(3).subscribe(print_value)
# print('-- Buffer with time')

print('-- Group by')

def key_selector(x: int) -> str:
     if 0 == x % 2 :
         return 'even'
     return 'odd'

def subscribe_group_observable(group_observable):
    def print_count(count):
        print('Group Observable Key "{}" contains {} items'.format(group_observable.key, count))
    group_observable.count().subscribe(print_count)

groups = Observable.from_(range(randint(1, 100000))).group_by(key_selector)
groups.subscribe(subscribe_group_observable)

print('-- Max')
Observable.from_([1, 2, 3, 4, 12, 3, 3, -10]).max(lambda x, y: x - y).subscribe(print_value)


test_scheduler.start()
