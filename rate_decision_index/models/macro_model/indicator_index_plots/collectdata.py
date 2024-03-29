import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import quandl
from sklearn.preprocessing import MinMaxScaler

quandl.ApiConfig.api_key = "kVFwRskyFgKCs3HURnYV"


def get_data2(indicators, start, end):
    df = pd.DataFrame()
    scaler = MinMaxScaler()
    for indicator in indicators:
        name = "FRED/" + indicator
        mydata = quandl.get(name, start_date=start, end_date=end, collapse='quarterly', transform = 'normalize')
        datecol=mydata.index
        mydata.index = pd.to_datetime(mydata.index).to_period('Q')
        mydata.rename(columns={'Value': indicator }, inplace=True)
        mydata[indicator] = pd.to_numeric(mydata[indicator])
        df = pd.concat([df, mydata], axis='columns')
        #print(indicator)
    df = df.fillna(method='ffill')
    return df

def collect_indicator_data(path="../../data/macroeconomic_indicators_data/"):  
    indicatorsR = ['GDPC1', 'PCEC96', 'GPDIC1', 'GCEC1', 'NETEXC']
    dfR = get_data2(indicators=indicatorsR, start='2004-01-01', end='')
    dfR.to_csv(f"{path}/macro_gdp_data.csv", index=True)

    indicators_employment = ['PAYEMS', 'USPRIV', 'CES9091000001', 'USCONS', 'MANEMP']
    dfEI = get_data2(indicators=indicators_employment, start='2004-01-01', end='')
    dfEI.to_csv(f"{path}/macro_employment_data.csv", index=True)

    indicators_inflation = ['MEDCPIM158SFRBCLE','CPIAUCSL','CPIFABSL', 'CPIAPPSL', 'CPIMEDSL', 'CPIHOSSL', 'CPITRNSL', 'CPIEDUSL', 'CPIRECSL', 'CPIOGSSL']
    df_inflation = get_data2(indicators=indicators_inflation, start='2004-01-01', end='')
    df_inflation.to_csv(f"{path}/macro_inflation_data.csv", index=True)

    print("All indicators data collected!")

if __name__ == "__main__":
    collect_indicator_data()