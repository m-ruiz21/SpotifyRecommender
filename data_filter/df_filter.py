import pandas as pd
from cleantext import clean

def get_data():
    df = pd.read_csv('./data/playlist_features.csv')
    return df


def get_rid_of_empty(df):
    for index, row in df.iterrows():
        name = row['name']
        if name == '':
            df.drop(index, inplace=True)


def clean_df(df):
    for index, row in df.iterrows():
        name = row['name']
        name = clean(name, lower=True, no_emoji=True)
        df.at[index, 'name'] = name


df = get_data()
get_rid_of_empty(df)
clean_df(df)

df.to_csv('./data/playlist_features_filtered.csv', index=False)