import datetime as dt 
from datetime import date
import matplotlib.pyplot as plt
import pandas as pd
import quandl
import numpy as np
from config import quandl_apikey
import requests
from sqlalchemy import create_engine
import plotly.graph_objects as go
import plotly
from matplotlib.ticker import FuncFormatter
import mplfinance as mpf
import matplotlib.dates as mdates


ohlc_url = 'static/img/ohlc_mpf.png'
mva5d_url = 'static/img/5d-wk-close.png'
mva20d_url = 'static/img/20d-wk-close.png'
mvawks_url = 'static/img/wk-close-ma.png'
ocl_url = 'static/img/ohlc.png'
weekly_vol_url = 'static/img/volume_weekly.png'
dr_url = 'static/img/dr.png'



def millions(x, pos):
    'The two args are the value and tick position'
    return '$%1.1fM' % (x*1e-6)




def getStock(target_stock):
    pstock = target_stock
    time_api = f"https://www.quandl.com/api/v3/datasets/WIKI/{pstock}/data.json?api_key={quandl_apikey}"
    tquery_stock = requests.get(time_api)
    stock_json = tquery_stock.json()
    df = pd.DataFrame(stock_json['dataset_data']['data'],columns= stock_json['dataset_data']['column_names'])
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index(df['Date'],drop=True)
    last_day = df.index[0]
    years = 2
    days_per_year = 365.24
    after_date = last_day - dt.timedelta(days=(years*days_per_year))
    #targets index. do not need to specify
    df2 = df.truncate(after = after_date)
    df2 = df2.rename(columns={'Ex-Dividend':'ExDividend', 'Split Ratio':'SplitRatio','Adj. Open':'AdjOpen','Adj. High':'AdjHigh','Adj. Low':'AdjLow','Adj. Close':'AdjClose','Adj. Volume':'AdjVolume'})
    #Add stock ticker column
    df['Ticker'] = pstock
    #before transfomration the dtype is object. 
    df['Date'] = pd.to_datetime(df['Date'])
    #volume mva
    volume_price = df2['AdjVolume']
    df2['Vol_10wk_ma'] = volume_price.rolling(window=50).mean()
    #close mva calculation
    close_price = df2['AdjClose']
    df2['Close_10wk_ma'] = close_price.rolling(window=70).mean()
    df2['Close_40wk_ma'] = close_price.rolling(window=280).mean()
    df2['Close_5d_ma'] = close_price.rolling(window=5).mean()
    df2['Close_10d_ma'] = close_price.rolling(window=10).mean()
    df2['Close_20d_ma'] = close_price.rolling(window=20).mean()
    #Creating Daily lag
    df2['DailyLag'] = df2['AdjClose'].shift(1)
    df2.head()
    #Daily Return rate
    df2['DailyReturn'] = (df2['DailyLag']/df2['AdjClose']) -1
    df2_weekly = df2.resample("W").sum()["Volume"]
    df2_weekly_clean = pd.DataFrame(df2_weekly)
    df2_weekly_clean.index = pd.to_datetime(df2_weekly_clean.index, format="%Y-%m-%d")
    volume_price_weekly = df2_weekly_clean['Volume']
    df2_weekly_clean['TenWeek'] = volume_price_weekly.rolling(window=10).mean()
    df2_weekly_clean['Date'] = df2_weekly_clean.index
    formatter = FuncFormatter(millions)
    x_axis_vol_weekly = df2_weekly_clean['Volume']
    y_axis = df2_weekly_clean['Date']
    x_axis_ma = df2_weekly_clean['TenWeek']
    
    #weekly volume
    figure, ax = plt.subplots()
    ax.yaxis.set_major_formatter(formatter)
    ax.bar(y_axis,x_axis_vol_weekly,color='b',label='Volume by Weekly')
    ax.plot(y_axis,x_axis_ma, color='r',label='10-week MVA')
    ax.grid(color='white')
    ax.set_title(f'Weekly Volume',size = 50)
    ax.set_xlabel('Date',fontsize = 50)
    ax.set_ylabel('Closing Prices',fontsize = 50)
    ax.set_facecolor('lightblue')
    figure.set_figheight(25)
    figure.set_figwidth(60)
    plt.legend(loc='best',prop={'size':40})
    ax.tick_params(axis='both', labelsize=40,size=80)
    plt.savefig(weekly_vol_url)
    
    #moving averages
    x_axis_5d = df2['Close_5d_ma']
    x_axis_10d = df2['Close_10d_ma']
    x_axis_20d = df2['Close_20d_ma']
    x_axis_10week = df2['Close_10wk_ma']
    x_axis_40week = df2['Close_40wk_ma']
    x_axis_close = df2['Close']
    y_axis = df2['Date']
    
    #moving average 20 days
    figure, ax = plt.subplots(figsize=(50,25))
    ax.plot(y_axis,x_axis_20d,linestyle="--",color='r',label='20-Day',linewidth=4)
    ax.plot(y_axis,x_axis_10week,color='b',label='10-Week MVA',linewidth=4)
    ax.plot(y_axis,x_axis_40week,color='purple',label='40-Week MVA',linewidth=4)
    ax.plot(y_axis,x_axis_close,color='green',label='Close Price Ticks',linewidth=4)
    ax.grid(color='white')
    ax.set_title(f'Closing Price and Moving Average (20Days)',size = 60)
    ax.set_xlabel('Date',fontsize = 60)
    ax.set_ylabel('Closing Prices',fontsize = 60)
    ax.set_facecolor('lightblue')
    plt.legend(loc='best',prop={'size':40})
    ax.tick_params(axis='both', labelsize=40,size=75)
    plt.savefig(mva20d_url)
    
    #moving average 5 days
    figure, ax = plt.subplots()
    ax.plot(y_axis,x_axis_5d,linestyle='--',color='r',label='5-Day MVA',linewidth=4)
    ax.plot(y_axis,x_axis_10week,color='b',label='10-Week MVA',linewidth=4)
    ax.plot(y_axis,x_axis_40week,color='purple',label='40-Week MVA',linewidth=4)
    ax.plot(y_axis,x_axis_close,color='green',label='Close Price Ticks',linewidth=4)
    ax.grid(color='white')
    ax.set_title(f'Closing Price and Moving Average (5Days)',size = 60)
    ax.set_xlabel('Date',fontsize = 60)
    ax.set_ylabel('Closing Prices',fontsize = 60)
    ax.set_facecolor('lightblue')
    figure.set_figheight(25)
    figure.set_figwidth(50)
    plt.legend(loc='best',prop={'size':40})
    ax.tick_params(axis='both', labelsize=40,size=75)
    plt.savefig(mva5d_url)
    

    #Open High Close
    x_axis_open = df2['Open']
    x_axis_high = df2['High']
    x_axis_low = df2['Low']
    x_axis_close = df2['Close']
    y_axis = df2['Date']
    figure, ax = plt.subplots()
    ax.scatter(y_axis,x_axis_high,marker="o",color='r',label='High',s=80)
    ax.scatter(y_axis,x_axis_low,marker='X',color='g',label='Low',s=100)
    ax.plot(y_axis,x_axis_close,label='Close',linewidth=4)
    ax.grid(color='white')
    ax.set_title(f'Open, High, Low, Close',size = 60)
    ax.set_xlabel('Date',fontsize = 40)
    ax.set_ylabel('Prices',fontsize = 40)
    ax.set_facecolor('lightblue')
    figure.set_figheight(20)
    figure.set_figwidth(40)
    plt.legend(loc='best',prop={'size':40})
    ax.tick_params(axis='both', labelsize=40, size=75)
    plt.savefig(ocl_url)

    #DailyReturn rate
    x_axis_dr = df2['DailyReturn']
    y_axis = df2['Date']
    figure, ax = plt.subplots()

    ax.plot(y_axis,x_axis_dr,color='r',label='DailyReturn',linewidth=2)
    ax.axhline(linewidth=2, color='b')
    ax.grid(color='white')
    ax.set_title(f'DailyReturns (Historical)',size = 60)

    ax.set_xlabel('Date',fontsize = 40)
    ax.set_ylabel('Return Rate ',fontsize = 40)
    ax.set_facecolor('lightblue')
    figure.set_figheight(20)
    figure.set_figwidth(45)
    plt.legend(loc='best',prop={'size':40})
    ax.tick_params(axis='both', labelsize=40, size=75)
    plt.savefig(dr_url)


    #ohlc MPF#
    df3 = df2[['Open','High','Low','Close','Volume']]
    
    mpf.plot(df3[:100], figratio=(45,15),figscale=0.8, type='candle', style='mike',
            title=f'{pstock} Analysis',
            ylabel='Price ($)',
            ylabel_lower='Shares \nTraded',
            volume=True, 
            mav=(10,20,40), 
            savefig=f'{ohlc_url}')



    df2.to_csv("data/df2.csv")
    df2_weekly_clean.to_csv("data/df2_weekly_clean.csv")
    
    to_database = {

        "stock":pstock,
        "wkly_vol":weekly_vol_url,
        "5dmva": mva5d_url,
        "20dmva": mva20d_url,
        "week_ma": mvawks_url,
        "ocl": ocl_url,
        "ohlc_mpf":ohlc_url,
        "dr":dr_url

    }
    
    return to_database