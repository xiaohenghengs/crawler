import datetime
import requests
from foreign_exchange_rate.conf import config, currency
from foreign_exchange_rate.models.rate import Rate


def doForeignExchangeRateCrawling():
    """
    上海银行外汇汇率数据爬取
    """
    url = config['url']['bosc']
    try:
        rate = Rate()
        data = requests.get(url + str(datetime.datetime.now().timestamp()))
        json_data = data.json()['data']
        target_data = [x for x in json_data if x['currencyName'] in [c['currency_explain'] for c in currency]]
        for d in target_data:
            rate.bank = 'bosc'
            rate.currency = d['currency1']
            rate.currency_explain = d['currencyName']
            rate.buy_price = d['buyPrice']
            rate.sell_price = d['sellPrice']
            rate.unit = int(d['unit'])
            publish_time = d['createTime']
            rate.publish_time = datetime.datetime.strptime(publish_time, "%Y-%m-%dT%H:%M:%S").strftime(
                "%Y-%m-%d %H:%M:%S")
            if rate.validate_rate_is_exist():
                rate.make_list(rate.to_list())
        rate.save()
    except Exception as e:
        print(e)
        pass
