import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

Ini_date="2022-01-01"
End_date="2022-06-30"

VIX_db = yf.download("^VIX", start=Ini_date, end=End_date)
print(VIX_db[:3])
SP500Fut_db = yf.download("ES=F", start=Ini_date, end=End_date)
print(SP500Fut_db[:3])
SP500_db = yf.download("^GSPC", start=Ini_date, end=End_date)
print(SP500_db[:3])

VIX_db=pd.DataFrame(VIX_db['Close'])
SP500Fut_db=pd.DataFrame(SP500Fut_db['Close'])
SP500_db=pd.DataFrame(SP500_db['Close'])

'''
display(VIX_db.head(3))
display(SP500Fut_db.head(3))
display(SP500_db.head(3))
'''

VIX_db.reset_index(inplace=True)
VIX_db = (VIX_db.set_index('Date')
      .reindex(pd.date_range(Ini_date, End_date, freq='D'))
      .rename_axis(['Date'])
      .fillna(method='ffill')
      .dropna()
      .reset_index())


SP500Fut_db.reset_index(inplace=True)
SP500Fut_db = (SP500Fut_db.set_index('Date')
      .reindex(pd.date_range(Ini_date, End_date, freq='D'))
      .rename_axis(['Date'])
      .fillna(method='ffill')
      .dropna()
      .reset_index())

SP500_db.reset_index(inplace=True)
SP500_db = (SP500_db.set_index('Date')
      .reindex(pd.date_range(Ini_date, End_date, freq='D'))
      .rename_axis(['Date'])
      .fillna(method='ffill')
      .dropna()
      .reset_index())

fig, ax1 = plt.subplots(figsize=(10,3.5))
ax2 = ax1.twinx()
ax1.plot(SP500_db['Date'], SP500_db['Close'],label = "SP500", color='black')
ax1.plot(SP500_db['Date'], SP500Fut_db['Close'], label = "SP500Fut",linestyle='dashdot', color='orange')
ax2.plot(SP500_db['Date'], VIX_db['Close'],  label ="VIX",linestyle='dotted', color='red')
ax1.legend(loc='lower left')
ax2.legend(loc='upper left')
plt.show()

MergedData= pd.concat(
    objs=(iDF.set_index('Date') for iDF in (VIX_db, SP500_db, SP500Fut_db)),
    axis=1, 
    join='inner'
).reset_index()
MergedData.columns=['Date','Close_VIX','Close_SP','Close_SPF']
MergedData.head(3)

LimVixUp=30
LimVixDw=20
Stgy_DF=MergedData.copy()
Stgy_DF['Ret']=Stgy_DF['Close_SP']/Stgy_DF['Close_SP'].shift(1)-1
Stgy_DF['SigVixg30']=(0+(np.sign(Stgy_DF['Close_VIX']-LimVixUp)==1))
Stgy_DF['SigVixs20']=(0+(np.sign(LimVixDw-Stgy_DF['Close_VIX'])==1))
Stgy_DF['SigRetg+5']=np.nan
Stgy_DF['SigRets-5']=np.nan
Stgy_DF['InvestVal']=0
Stgy_DF['InvestOp']=np.nan
Stgy_DF['StrgRet']=0
Stgy_DF['StrgDecitions']=np.nan



###########################################################################
#### Loop #################################################################
###########################################################################

DecCount=0
SwichBuySell=0
for i in range(len(Stgy_DF)):
  #Strategy return calculation
  
  #print(i>=0)
  #print(Stgy_DF.loc[i,'InvestOp']!=np.nan)
  if i>0:
    #last signal sell
    if  np.isnan(Stgy_DF.loc[i,'InvestOp'])!=True and Stgy_DF.loc[i-1,'StrgDecitions']=='sell':
      Stgy_DF.loc[i,'StrgDecitions']='sell'
      Stgy_DF.loc[i,'InvestVal']=Stgy_DF.loc[i-1,'InvestVal']
      print(Stgy_DF[i-1:i+2])
    elif np.isnan(Stgy_DF.loc[i,'InvestOp'])==True and Stgy_DF.loc[i-1,'StrgDecitions']=='sell':
      Stgy_DF.loc[i,'StrgDecitions']='sell'
      Stgy_DF.loc[i,'InvestOp']=Stgy_DF.loc[i-1,'InvestOp']
      Stgy_DF.loc[i,'InvestVal']=Stgy_DF.loc[i-1,'InvestVal']
      print(Stgy_DF[i-1:i+2])
    #last signal buy
    if np.isnan(Stgy_DF.loc[i,'InvestOp'])!=True and Stgy_DF.loc[i-1,'StrgDecitions']=='buy':
      Stgy_DF.loc[i,'StrgDecitions']='buy'
      Stgy_DF.loc[i,'InvestVal']=Stgy_DF.loc[i-1,'InvestVal']*(1+Stgy_DF.loc[i,'Ret'])
      print(Stgy_DF[i-1:i+2])
    elif np.isnan(Stgy_DF.loc[i,'InvestOp'])==True and Stgy_DF.loc[i-1,'StrgDecitions']=='buy':
      Stgy_DF.loc[i,'StrgDecitions']='buy'
      Stgy_DF.loc[i,'InvestOp']=Stgy_DF.loc[i-1,'InvestOp']
      Stgy_DF.loc[i,'InvestVal']=Stgy_DF.loc[i-1,'InvestVal']*(1+Stgy_DF.loc[i,'Ret'])
      print(Stgy_DF[i-1:i+2])

  #Strategy returns calculation
  if np.isnan(Stgy_DF.loc[i,'InvestOp'])==True:
    Stgy_DF.loc[i,'StrgRet']=0
  else:
    Stgy_DF.loc[i,'StrgRet']=Stgy_DF.loc[i,'InvestVal']/Stgy_DF.loc[i,'InvestOp']-1
  if i==28:
    print(i)

  if Stgy_DF.loc[i,'SigVixg30']==1:
    #buy
    if DecCount==0:
      Stgy_DF.loc[i,'StrgDecitions']='buy'
      Stgy_DF.loc[i,'InvestVal']=1
      Stgy_DF.loc[i,'InvestOp']=Stgy_DF.loc[i,'InvestVal']
      Stgy_DF.loc[i+1,'InvestOp']=Stgy_DF.loc[i,'InvestVal']
      Stgy_DF.loc[i,'StrgRet']=Stgy_DF.loc[i,'InvestVal']/Stgy_DF.loc[i,'InvestOp']-1
      print(Stgy_DF[i-1:i+2])
      DecCount=+1
    elif DecCount>=0 and Stgy_DF.loc[i-1,'StrgDecitions']=='sell':
      Stgy_DF.loc[i,'StrgDecitions']='buy'
      Stgy_DF.loc[i,'InvestOp']=Stgy_DF.loc[i-1,'InvestOp']
      Stgy_DF.loc[i,'InvestVal']=Stgy_DF.loc[i,'InvestOp']
      Stgy_DF.loc[i+1,'InvestOp']=Stgy_DF.loc[i,'InvestVal']
      Stgy_DF.loc[i,'StrgRet']=Stgy_DF.loc[i,'InvestVal']/Stgy_DF.loc[i,'InvestOp']-1
      print(Stgy_DF[i-1:i+2])
      DecCount=+1
  
  #Stop loss - Take profit
  if Stgy_DF.loc[i,'StrgRet']<-0.05:
    Stgy_DF.loc[i,'SigRets-5']=1
  else:
    Stgy_DF.loc[i,'SigRets-5']=0
  if Stgy_DF.loc[i,'StrgRet']>0.05:
    Stgy_DF.loc[i,'SigRetg+5']=1
  else:
    Stgy_DF.loc[i,'SigRetg+5']=0
  
  #print(Stgy_DF.loc[i-1,'StrgDecitions']=='buy')
  if DecCount>0 and (Stgy_DF.loc[i,'SigVixs20']==1 or Stgy_DF.loc[i,'SigRetg+5']==1 or Stgy_DF.loc[i,'SigRets-5']==1):
    #sell
    if Stgy_DF.loc[i-1,'StrgDecitions']=='buy':
      Stgy_DF.loc[i,'StrgDecitions']='sell'
      Stgy_DF.loc[i,'InvestOp']=Stgy_DF.loc[i-1,'InvestOp']
      Stgy_DF.loc[i,'InvestVal']=Stgy_DF.loc[i-1,'InvestVal']*(1+Stgy_DF.loc[i,'Ret'])
      Stgy_DF.loc[i+1,'InvestOp']=Stgy_DF.loc[i,'InvestVal']
      Stgy_DF.loc[i,'StrgRet']=Stgy_DF.loc[i,'InvestVal']/Stgy_DF.loc[i,'InvestOp']-1
      print(Stgy_DF[i-1:i+2])
      DecCount=+1
  print(Stgy_DF[i-1:i+2])
      