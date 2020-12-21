import os
from datetime import timedelta
from os import listdir
from datetime import datetime
import json
import sys
import numpy as np
from talib import abstract
import talib
from sklearn.preprocessing import MinMaxScaler
import pickle
import pandas as pd
from pandas_datareader import data as dtr
from datetime import date, timedelta
def get_time_li(date_,day_nums):
    time_delta=1
    day_count=0
    date_list=[]
#     file_dir="/home/mlb/res/stock/twse/json/"
    file_dir="stock_price/"
    date_time = datetime.strptime(date_, '%Y-%m-%d')
    while True:
        temp_date=(date_time+timedelta(days=-1*time_delta)).strftime("%Y-%m-%d")
        filepath=file_dir+temp_date+'.json'
        if os.path.isfile(filepath):
            day_count+=1
            date_list.append(temp_date)
        if day_count==day_nums:
            return date_list
            break 
        time_delta+=1
def get_dates():
#     mypath = "/home/mlb/res/stock/twse/json/"
    mypath="stock_price/"
    # 取得所有檔案與子目錄名稱
    files = listdir(mypath)
    files.sort()         ##4113天
    dates=[ele.strip('.json') for ele in files]
    return dates
def check_stock_exist(ele,data):
    if ele in data and data[ele]['close']!='NULL' and data[ele]['open']!='NULL' and data[ele]['volume']!='NULL'and data[ele]['open']!='None' and data[ele]['close']!='None' and data[ele]['adj_close']!='NULL' and data[ele]['adj_close']!='None':
        return True
    else:
        return False

def get_all_criteria(df):
    ta_list = talib.get_functions()
    for x in ta_list:
        try:
            # x 為技術指標的代碼，透過迴圈填入，再透過 eval 計算出 output
            output = eval('abstract.'+x+'(df)')
            # 如果輸出是一維資料，幫這個指標取名為 x 本身；多維資料則不需命名
            output.name = x.lower() if type(output) == pd.core.series.Series else None
            # 透過 merge 把輸出結果併入 df DataFrame
            df = pd.merge(df, pd.DataFrame(output), left_on = df.index, right_on = output.index)
            df = df.set_index('key_0')
        except:
            pass
#             print(x," fail")
    return df
def get_shift_day_with_criteria(use_day,df):
    df_new=df.copy()
    move_li=list(df_new.columns)
    for day in range(1,use_day):
        for ele in move_li:
            df_new[ele+str(use_day-day)]= df_new[ele].shift(day)
    return df_new

def filetr_nan_drop_index(df):
#     print('Total:',len(df))
    for ele in list(df.columns):
        if df[ele].isnull().sum() >len(df)/2:
#             print("Drop:",ele)
            df=df.drop([ele],axis=1)
    stock_cleanData = df.copy()
    df.head()
    stock_cleanData.dropna(inplace=True)
    stock_cleanData.volume = stock_cleanData.volume.astype(float)
    return stock_cleanData
def scale_data(stock_cleanData,name,scale_type):
    scaler = MinMaxScaler(feature_range=(0.1, 1.1))  ##price本身
    feature_li=[ele for ele in list(stock_cleanData.columns) if ele not in ['high','low','open','close']]   
    stock_cleanData[feature_li]=scaler.fit_transform(stock_cleanData[feature_li])

    scaler_price = MinMaxScaler()                   ##其他param
    scaler_price.fit([[stock_cleanData['high'].max()],[stock_cleanData['low'].min()]])
    if scale_type==1:
        scaler_dir='scaler/'+use_scaler[name]
#         print("use_scaler_model")
        with open(scaler_dir, 'rb') as f:
            scaler_price= pickle.load(f)
    stock_cleanData[['high','low','open','close']]=scaler_price.transform(stock_cleanData[['high','low','open','close']])
    return stock_cleanData

def get_data(stock_number,date):
    data_=dtr.DataReader(stock_number, "yahoo", "2019-01-01",date)
    data_=data_.rename(columns={'High':'high','Low':'low','Open':'open','Close':'close','Volume':'volume'})
    df= data_[data_.columns.tolist()[:-1]]
    return df
def strategy_tw50(date_,current_date):
    models=listdir('models/')
    use_model={}
    stock_code=[]
    for ele in models:
        token=ele.split('_')
        if token[4]!='nan':
            if float(token[4])>0.5:
                use_model[token[2]]=ele
                stock_code.append(token[2])
    scalers=listdir('scaler/')
    use_scaler={ele.split('_')[0]:ele for ele in scalers}
    
    stock_data={ele:get_data(ele+'.TW',date_) for ele in stock_code}  
    print("stock_code",stock_code)
    buy_list=[]
    for stock in stock_data:
        try:
            t1=stock_data[stock]
            t1=get_all_criteria(t1)
            t1=get_shift_day_with_criteria(3,t1)
            clean_data=filetr_nan_drop_index(t1)
            print(stock)
            clean_data=scale_data(clean_data,stock,0)

            current_data=clean_data.iloc[-1]
            predict_input=pd.DataFrame(dict(current_data),index=[0])
            model_dir='models/'+use_model[stock]
            with open(model_dir, 'rb') as f:
                model = pickle.load(f)
                output_y = model.predict(predict_input)
                if output_y[0]:
                    buy_list.append(stock)
        except:
            print("error:",stock)
    decision_set = []
    for ele in buy_list:
        curr_stock =stock_data[ele]
        close_price=curr_stock.close.tolist()[-1]
        curr_decision = {
        "code": ele,
        "life": 1,
        "type": "buy",
        "weight": 1,
        "open_price": float(close_price),
        "close_high_price":float(close_price)*1.02,
        "close_low_price":float(close_price)*0.999      
        }
        decision_set.append(curr_decision)
    print(date_, decision_set)
    json.dump(decision_set, open(f'strategy/{current_date}_{current_date}.json', 'w'), indent=4)   
    return stock_data
now = datetime.now()
current_date=now.strftime("%Y-%m-%d")
pre_day=now-timedelta(1)
pre_date=pre_day.strftime("%Y-%m-%d")
print("date:",current_date)
strategy_tw50(pre_date,current_date)