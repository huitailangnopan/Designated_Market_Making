import pandas as pd
from sqlitedict import SqliteDict

def sql_to_list(db):
    return [db[item] for item in db]

def sql_to_pd(db):
    assets = db[1].keys()
    record = {i: pd.DataFrame() for i in assets}
    for item in db:
        for i in assets:
            record[i] = pd.concat([record[i], pd.DataFrame([db[item][i]])], ignore_index=True)
    return record

def quotedspread(df):
    df['mid_price'] = (df['ask1_price'] + df['bid1_price']) / 2
    df['quotedspread'] = (df['ask1_price'] - df['bid1_price']) / df['mid_price']
    df['quotedspread'].fillna(0, inplace=True)
    return df

def effectivespread(df):
    df['effectivespread'] = df.apply(lambda row: (-1 if row['initiator'] == 'SELLER' else 1) * (row['deal_price'] - row['mid_price']) / row['mid_price'], axis=1)
    return df