import sys
import random

from rx import Observable
from rx.subjects import Subject
from rx.concurrency import QtScheduler

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTableWidget, QTableWidgetItem, QGridLayout, QLabel, QLineEdit, QFormLayout

class StockOverviewTable(QTableWidget):
    def __init__(self, *args, **kwargs):
        stock_prices_stream =kwargs.pop('stock_prices_stream')
        QTableWidget.__init__(self, *args, **kwargs)
        self.setRowCount(0)
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(['Symbol', 'Name', 'Buy Price', 'Sell Price'])
        self.setColumnWidth(0, 50)
        self.setColumnWidth(0, 200)
        self.setColumnWidth(0, 100)
        self.setColumnWidth(0, 100)
        self.horizontalHeader().setStretchLastSection(True)
        self.setSortingEnabled(True)
        stock_prices_stream.subscribe(self._create_or_update_stock_row)

    def _find_matching_row_index(self, stock_row):
        # row[0] will be the Symbol
        matches = self.findItems(stock_row[0], QtCore.Qt.MatchExactly)
        if 0 == len(matches):
            self.setRowCount(self.rowCount() + 1)
            return self.rowCount() - 1
        return self.indexFromItem(matches[0]).row()

    def _create_or_update_stock_row(self, stock_row):
        row = self._find_matching_row_index(stock_row)

        column_index = 0
        for column in stock_row:
            self.setItem(row, column_index, QTableWidgetItem(str(column)))
            column_index += 1

class TransactionForm(QWidget):
    def __init__(self, *args, **kwargs):
        self._orders_stream = Subject()
        self._validator = None
        QWidget.__init__(args, kwargs)
        self._setup_form()
        self._connect_events()
        self._subsribe_to_stream()

    def _setup_form(self):
        self._symbol_input = QLineEdit()
        self._symbol_error = QLabel()
        self._price_input = QLineEdit()
        self._price_error = QLabel()
        self._ok_button = QPushButton('Post Order')
        self._layout = QFormLayout(self)
        self._layout.addRow('Symbol: ', self._symbol_input)
        self._layout.addRow(self._symbol_error_label)
        self._layout.addRow('Price: ', self._price_input)
        self._layout.addRow(self._price_error_label)
        self._layout.addRow(self._ok_button)
        self._clear_form()

    def _connect_events(self):
        pass

    def _subscribe_to_stream(self):
        pass

class HelloWorld(QWidget):
    def __init__(self, *args, **kwargs):
        stock_prices_stream = kwargs.pop('stock_prices_stream')
        QWidget.__init__(self, *args, **kwargs)

        self._events = Subject()
        self._setup_window()
        self._layout = QGridLayout(self)
        self._overview_table = StockOverviewTable(stock_prices_stream=stock_prices_stream)
        self._layout.addWidget(self._overview_table, 0, 0)
        self._layout.addWidget(self._form, 0, 2)
        self._layout.setColumnStretch(0, 2)

    def _setup_window(self):
        self.resize(640, 320)
        self.move(350, 200)
        self.setWindowTitle('hello world')

    def get_orders(self):
        return self._form.orders_stream

REFRESH_STOCK_INTERVAL = 100

def random_stock(x):
    symbol_names = [
        ['ABC', 'Abc Manufacturing'],
        ['DEF', 'Desert Inc.'],
        ['GHI', 'Ghi Ghi Inc.'],
        ['A', 'A Plus Consulting'],
        ['GS', 'Great Security Inc'],
        ['GO', 'Go Go Consulting'],
    ]
    stock = random.choice(symbol_names)
    return [
        stock[0],
        stock[1],
        round(random.uniform(21, 22), 2),
        round(random.uniform(20, 21), 2),
    ]

if '__main__' == __name__:
    app = QApplication(sys.argv)
    scheduler = QtScheduler(QtCore)
    stock_prices = Observable.interval(REFRESH_STOCK_INTERVAL, scheduler).map(random_stock).publish()
    hello_world = HelloWorld(stock_prices_stream=stock_prices)
    hello_world.get_orders().subscribe(lambda x: print(x))
    stock_prices.connect()
    hello_world.show()
    sys.exit(app.exec_())
