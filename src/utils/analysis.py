import pandas as pd
import numpy as np
from sqlitedict import SqliteDict


def sql_to_list(db):
    price = []
    for item in db:
        price.append(db[item])
    return price


def sql_to_pd(db):
    record = {}
    assets = db[1].keys()
    for i in assets:
        record[i] = pd.DataFrame()
    for item in db:
        each_timeframe = db[item]
        for i in assets:
            each_timeframe_asset = each_timeframe[i]
            df_dictionary = pd.DataFrame([each_timeframe_asset])
            record[i] = pd.concat([record[i], df_dictionary], ignore_index=True)
    return record

def quotedspread(df):
    """
    (a_t-b_t)/m_t
    used for analyzing market order book
    """
    for i in range(len(df)):
        mid_price = (df.loc[i,'ask1_price']+df.loc[i,'bid1_price'])/2
        df.loc[i,'mid_price'] = mid_price
        df.loc[i,'quotedspread'] = (df.loc[i,'ask1_price'] - df.loc[i,'bid1_price'])/mid_price if mid_price !=0 else 0
    return df

def effectivespread(df):
    """
    (q_t (p_t-m_t ))/m_t
    used for executed orders
    """
    for i in range(len(df)):
        q_t = -1 if df.loc[i,'initiator'] == 'SELLER' else 1
        p_t = df.loc[i,'deal_price']
        m_t = df.loc[i,'mid_price']
        df.loc[i,'effectivespread'] = q_t*(p_t-m_t)/m_t
    return df

