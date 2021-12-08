import unittest
from foreign_exchange_rate.boc.main import doForeignExchangeRateCrawling


class TestCrawler(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_crawlerBocForeignExchangeRate(self):
        doForeignExchangeRateCrawling()


if __name__ == '__main__':
    unittest.main()
