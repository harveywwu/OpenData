# encoding: utf-8
import datetime
from .spot_agent import SpotAgent

spot_agent = SpotAgent()

def get_commodity_spot_indicator():
    return spot_agent.get_commodity_spot_indicator()

def get_commodity_spot_indicator_data(indicator_id, start_date = None, end_date = None):
    if end_date == None:
        end_date = datetime.date.today()
    if start_date == None:
        start_date = end_date - datetime.timedelta(days = 365)
    return spot_agent.get_commodity_spot_indicator_data(indicator_id, start_date, end_date)

