# encoding: utf-8
from .aemo_agent import AEMOAgent
import pandas as pd
import datetime

aemo_agent = AEMOAgent()

def monthlist(start_date, end_date):
    total_months = lambda dt: dt.month + 12 * dt.year
    mlist = []
    for tot_m in xrange(total_months(start_date)-1, total_months(end_date)):
        y, m = divmod(tot_m, 12)
        mlist.append(datetime.datetime(y, m+1, 1).strftime("%Y%m"))
    return mlist

def get_curr_price_demand(region):
    return aemo_agent.get_curr_price_demand(region)

def get_hist_price_demand(region = 'NSW', start_date = None, end_date = None):
    if end_date == None:
        end_date = datetime.date.today() - datetime.timedelta(days=30)
    elif type(end_date).__name__ != 'date':
        end_date = end_date.replace('/', '')
        end_date = end_date.replace('-', '')
        end_date = datetime.datetime.strptime(end_date, "%Y%m%d")
    if start_date == None:
        start_date = end_date - datetime.timedelta(days=30)
    elif type(start_date).__name__ != 'date':
        start_date = start_date.replace('/', '')
        start_date = start_date.replace('-', '')
        start_date = datetime.datetime.strptime(start_date, "%Y%m%d")
    contmth_list = monthlist(start_date, end_date)
    df_list = pd.DataFrame()
    for contmth in contmth_list:
        df, msg = aemo_agent.get_hist_price_demand(region, contmth)
        if len(df)>0:
            df_list = df_list.append(df)
    if len(df_list) > 0:
        start_time = datetime.datetime.combine(start_date, datetime.time(0,0))
        end_time = datetime.datetime.combine(end_date + datetime.timedelta(days=1), datetime.time(0,0))
        df_list = df_list[(df_list['SETTLEMENTDATE']>start_time)&(df_list['SETTLEMENTDATE']<=end_time)]
        df_list.reset_index(drop=True, inplace = True)
        msg = ""
    else:
        msg = "No data loaded"
    return df_list, msg


