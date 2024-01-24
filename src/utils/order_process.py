from sqlitedict import SqliteDict
import os


def read(current_time):
    db = SqliteDict("exchange.sqlite",tablename="market_trade")
    orderbook = list(db[current_time].values())[0]
    db.close()
    return orderbook

def submit(current_time,myorder):
    db = SqliteDict("exchange.sqlite",tablename="mm1")
    db[current_time] = myorder
    db.commit()
    db.close()