# encoding: utf-8
from opendatatools.common import RestAgent
import io
import pandas as pd
import datetime

class AEMOAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    def get_curr_price_demand(self, region):
        url = "http://www.nemweb.com.au/mms.GRAPHS/GRAPHS/GRAPH_30{region}1.csv".format(region = region)
        res = self.do_request(url)
        if res:
            df = pd.read_csv(io.StringIO(res.decode('utf-8')))
            df['SETTLEMENTDATE'] = df['SETTLEMENTDATE'].apply(lambda x: datetime.datetime.strptime(x, "%Y/%m/%d %H:%M:%S"))
            msg = ""
        else:
            df = pd.DataFrame()
            msg = "Data Link Error"
        return df, msg

    def get_hist_price_demand(self, region, cont_mth):
        if '-' in cont_mth:
            cont_mth = cont_mth.replace('-', '')
        elif '/' in cont_mth:
            cont_mth = cont_mth.replace('/', '')
        elif type(cont_mth).__name__ == 'date':
            cont_mth = str(cont_mth.year * 100 + cont_mth.month)
        if len(cont_mth)>6:
            cont_mth = cont_mth[:6]
        url = "http://www.nemweb.com.au/mms.GRAPHS/data/DATA{contmth}_{region}1.csv".format(contmth = cont_mth, \
                                                                                            region = region)
        res = self.do_request(url)
        if res:
            df = pd.read_csv(io.StringIO(res.decode('utf-8')))
            df['SETTLEMENTDATE'] = df['SETTLEMENTDATE'].apply(lambda x: datetime.datetime.strptime(x, "%Y/%m/%d %H:%M:%S"))
            msg = ""
        else:
            df = pd.DataFrame()
            msg = "Data is not available"
        return df, msg