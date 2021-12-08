from lib.mysql_operate import MySqlOperate


class Rate:
    def __init__(self, bank=None, currency=None,
                 currency_explain=None, buy_price=None,
                 sell_price=None, unit=None, publish_time=None):
        self.__bank = bank
        self.__currency = currency
        self.__currency_explain = currency_explain
        self.__buy_price = buy_price
        self.__sell_price = sell_price
        self.__unit = unit
        self.__publish_time = publish_time
        self.__rate_list = []

    @property
    def bank(self):
        return self.__bank

    @bank.setter
    def bank(self, bank):
        self.__bank = bank

    @property
    def currency(self):
        return self.__currency

    @currency.setter
    def currency(self, currency):
        self.__currency = currency

    @property
    def currency_explain(self):
        return self.__currency_explain

    @currency_explain.setter
    def currency_explain(self, currency_explain):
        self.__currency_explain = currency_explain

    @property
    def buy_price(self):
        return self.__buy_price

    @buy_price.setter
    def buy_price(self, buy_price):
        self.__buy_price = buy_price

    @property
    def sell_price(self):
        return self.__sell_price

    @sell_price.setter
    def sell_price(self, sell_price):
        self.__sell_price = sell_price

    @property
    def unit(self):
        return self.__unit

    @unit.setter
    def unit(self, unit):
        self.__unit = unit

    @property
    def publish_time(self):
        return self.__publish_time

    @publish_time.setter
    def publish_time(self, publish_time):
        self.__publish_time = publish_time

    def to_list(self):
        return [self.__bank, self.__currency, self.__currency_explain, self.__buy_price, self.__sell_price, self.__unit,
                self.__publish_time]

    def to_tuple(self):
        return (self.__bank, self.__currency, self.__currency_explain, self.__buy_price, self.__sell_price, self.__unit,
                self.__publish_time)

    def make_list(self, record):
        self.__rate_list.append(record)

    def validate_rate_is_exist(self):
        with MySqlOperate() as db:
            sql = """
            SELECT * 
            FROM foreign_exchange_rate 
            WHERE bank = '%s'
                AND currency = '%s'
                AND currency_explain = '%s'
                AND buy_price = %s
                AND sell_price = %s
                AND unit = %s
                AND publish_time = '%s'
            """
            records = db.query_all(sql % self.to_tuple())
            return not len(records) > 0

    def save(self):
        if len(self.__rate_list) > 0:
            with MySqlOperate() as db:
                sql = """
                INSERT INTO foreign_exchange_rate (bank,currency,currency_explain,buy_price,sell_price,unit,publish_time)
                 VALUES (%s,%s, %s, %s,%s, %s, %s)
                """
                db.executemany_sql(sql, self.__rate_list)
