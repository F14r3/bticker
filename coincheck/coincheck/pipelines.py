# -*- coding: utf-8 -*-
import logging
import traceback

from sqlalchemy.orm import sessionmaker
from models import Market, Price, db_connect

logger = logging.getLogger('coincheck')


class CoincheckPipeline(object):
    """ Coincheck pipeline for storing scraped items in the database """

    def __init__(self):
        """ Initializes database connection and sessionmaker. """
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """ Save item in the database. """
        session = self.Session()
        deal = Price(**item)

        try:
            session.add(deal)
            session.commit()
        except Exception as ex:
            logger.error(ex)
            logger.error(traceback.format_exc())
            session.rollback()
            raise
        finally:
            session.close()

        return item


# from datetime import datetime
# import MySQLdb.cursors
# from scrapy.exceptions import DropItem
# from twisted.enterprise import adbapi
# import settings as mysettings

# class MySQLStorePipeline(object):
#     """A pipeline to store the item in a MySQL database.
#     This implementation uses Twisted's asynchronous database API.
#     """
#
#     def __init__(self):
#         cn = mysettings.DATABASE
#         self.dbpool = adbapi.ConnectionPool('MySQLdb',
#                                             host=cn['host'],
#                                             port=cn['port'],
#                                             db=cn['database'],
#                                             user=cn['username'],
#                                             passwd=cn['password'],
#                                             cursorclass=MySQLdb.cursors.DictCursor,
#                                             charset='utf8', use_unicode=True)
#
#     def process_item(self, item, spider):
#         # run db query in thread pool
#         d = self.dbpool.runInteraction(self._insert, item)
#         d.addErrback(self._handle_error, item, spider)
#         d.addBoth(lambda _: item)
#         return item
#
#     def _insert(self, tx, item):
#         # all this block run on it's own thread
#         now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
#         sql = "INSERT INTO trading_price (market_id, ask, bid, volume, created_at) " \
#               "VALUES ({}, {}, {}, {}, '{}')".format(item['market_id'], item['ask'], item['bid'], item['volume'], now)
#         print sql
#         tx.execute(sql)
#         log.msg("Item stored in db: %s" % item, level=log.DEBUG)
#
#     def _handle_error(self, failure, item, spider):
#         """Handle occurred on db interaction."""
#         log.err(failure)

# class CoincheckPipeline(object):
#     def process_item(self, item, spider):
#         return item
