import requests
from io import StringIO
import pandas as pd
import numpy as np
import time
import random
from datetime import timedelta, date

def crawler(datestr):
    try:      
        datestr = str(datestr)
        print('開始下載股價:', datestr)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALL',  headers = headers)
        df = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '}) 
                                         for i in r.text.split('\n') 
                                         if len(i.split('",')) == 17 and i[0] != '='])), header=0)
        return df,datestr   
    except:
        print('error')
        time.sleep(random.uniform(1, 3))#不要造成人家伺服器的負擔
    

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)
 
stock = pd.DataFrame()              
flag = 1 #開df存colname
start_dt = date(2015, 12, 28)
end_dt = date(2015, 12, 31)

for dt in daterange(start_dt, end_dt):
    if dt.weekday() <=5: 
        dt=dt.strftime("%Y%m%d")
        print(dt)
        if flag==1:
            try:
                df,datestr = crawler(dt)           
                stock['證券代號'] = 0
                stock['證券代號'] = df['證券代號']
                flag = 0
            except:
                print("no transaction")
        else:
            try:
                df,datestr = crawler(dt)                  
            except:
                print("今日無交易")
        stock[dt] = 0
        stock[dt] = df['收盤價']
        for i in range(len(stock)):
            stock[dt][i] = stock[dt][i].replace(',','') #ex 2,175
            if(stock[dt][i]!='--'):
                stock[dt][i] = float(stock[dt][i])
#n+1日才有profit
                
#Ri投資報酬率為= (今日收盤價-昨日收盤價) /昨日收盤價
ROI = pd.DataFrame(dtype=np.float)  
ROI['證券代號'] = 0
ROI['證券代號'] = df['證券代號']               
              
for i in range(2,len(stock.columns)):
    ROI[stock.columns[i]] = 0
    for j in range(len(stock)):
        ROI[stock.columns[i]][j] = float(ROI[stock.columns[i]][j])
        if (stock[stock.columns[i]][j]!='--' and stock[stock.columns[i-1]][j]!='--'):
            ROI[stock.columns[i]][j] = float((stock[stock.columns[i]][j] - stock[stock.columns[i-1]][j])/stock[stock.columns[i-1]][j])
