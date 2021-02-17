from Scraper.scraper import MintScraper
import pandas as pd
import json
import os
import numpy as np
from datetime import datetime
    
def convert_date(date):
    dt = datetime.strptime(date,'%B %Y')
    return dt.strftime('%Y%m%d')
    
# Load in the raw net worth data
json_path = 'data.json'
if input('Update from Mint? (y/n)'):
    mint_scraper = MintScraper()
    mint_scraper.connect()
    net_worth_data = mint_scraper.get_all_account_history()
    with open(json_path,'w+') as json_file: json.dump(net_worth_data,json_file)
else:
    with open(json_path,'r') as json_file: net_worth_data = json.load(json_file)


list_of_dfs=[]
for account_data in net_worth_data:
    s = account_data['source']
    n = account_data['name']
    title = f"Assets ({s}|{n})"
    data = account_data['data']
    df = pd.DataFrame.from_dict(data)
    df['Dates'] = df.apply(lambda row: convert_date(row['Dates']),axis=1)
    df = df.set_index("Dates")
    df = df.rename({'Dates':'Dates','Assets':title},axis=1)
    list_of_dfs.append(df)

combined_df = pd.concat(list_of_dfs,axis=1)
combined_df = combined_df.sort_index()
combined_df['Net Assets'] = combined_df.apply(lambda row: np.sum(row),axis=1)
combined_df.apply(lambda col: print(col),axis=0)
print(combined_df)
combined_df.to_csv('accounts.csv')
