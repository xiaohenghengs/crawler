import datetime

import requests
from bs4 import BeautifulSoup

from foreign_exchange_rate.conf import config, currency
from foreign_exchange_rate.models.rate import Rate


def doForeignExchangeRateCrawling():
    """
    中国银行外汇汇率数据爬取
    """
    url = config['url']['boc']
    now = datetime.date.today()
    try:
        rate = Rate()
        for pj in currency:
            params = {
                'erectDate': now,
                'nothing': now,
                'pjname': pj['currency_explain'],
                'head': 'head_620.js',
                'bottom': 'bottom_591.js'
            }
            webInfo = requests.get(url, params)
            soup = BeautifulSoup(webInfo.text, 'html.parser')
            table = soup.select('table')[1]
            tr = table.select('tr')[1]
            td = tr.select('td')
            ccy = td[0].text.strip()
            rate.bank = 'boc'
            rate.currency = [x for x in currency if x['currency_explain'] == ccy][0]['currency']
            rate.currency_explain = ccy
            rate.buy_price = td[1].text.strip()
            rate.sell_price = td[3].text.strip()
            rate.unit = 100
            publish_time = td[6].text.strip()
            rate.publish_time = datetime.datetime.strptime(publish_time, "%Y.%m.%d %H:%M:%S").strftime(
                "%Y-%m-%d %H:%M:%S")
            if rate.validate_rate_is_exist():
                rate.make_list(rate.to_list())
        rate.save()
    except Exception as e:
        print(e)
        pass
