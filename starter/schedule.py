import sys

sys.path.append(r'../../crawler')
from apscheduler.schedulers.blocking import BlockingScheduler

from foreign_exchange_rate.boc.main import doForeignExchangeRateCrawling as BOCForeignExchangeRateCrawling
from foreign_exchange_rate.bosc.main import doForeignExchangeRateCrawling as BOSCForeignExchangeRateCrawling

schedule = BlockingScheduler(timezone='Asia/Shanghai')


@schedule.scheduled_job('interval', id='crawling_boc_foreign_exchange_rate', minutes=5)
def crawlingBOCForeignExchangeRate():
    BOCForeignExchangeRateCrawling()


@schedule.scheduled_job('interval', id='crawling_bosc_foreign_exchange_rate', minutes=10)
def crawlingBOSCForeignExchangeRate():
    BOSCForeignExchangeRateCrawling()


if __name__ == '__main__':
    schedule.start()
