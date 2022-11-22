import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


StgyDf = pd.read_excel('D:\cursos\Maestria finanzas\S3_Trading\Proyecto\RawDataLTSM.xlsx')


StgyDf.drop(['Unnamed: 0'], axis=1,inplace=True)
StgyDf.dropna(inplace=True)
print(StgyDf.head(10))
StgyDf['Ret']=StgyDf['Close_SP']/StgyDf['Close_SP'].shift(1)-1
StgyDf['Signal']=np.sign(StgyDf['Pred']-StgyDf['Close_SP'])
StgyDf['InvestVal']=np.nan
StgyDf['InvestOp']=np.nan
StgyDf['StrgRet']=0
StgyDf['StrgDecitions']=np.nan
StgyDf.reset_index(inplace=True)
print(StgyDf.head(10))

DecCount=0
for i in range(len(StgyDf)):
    
    if i>0:
        #last signal sell
        if  np.isnan(StgyDf.loc[i,'InvestOp'])!=True and StgyDf.loc[i-1,'StrgDecitions']=='sell':
            StgyDf.loc[i,'StrgDecitions']='sell'
            StgyDf.loc[i,'InvestVal']=StgyDf.loc[i-1,'InvestVal']
            print(StgyDf[i-1:i+2])
        elif np.isnan(StgyDf.loc[i,'InvestOp'])==True and StgyDf.loc[i-1,'StrgDecitions']=='sell':
            StgyDf.loc[i,'StrgDecitions']='sell'
            StgyDf.loc[i,'InvestOp']=StgyDf.loc[i-1,'InvestOp']
            StgyDf.loc[i,'InvestVal']=StgyDf.loc[i-1,'InvestVal']
            print(StgyDf[i-1:i+2])
        #last signal buy
        if np.isnan(StgyDf.loc[i,'InvestOp'])!=True and StgyDf.loc[i-1,'StrgDecitions']=='buy':
            StgyDf.loc[i,'StrgDecitions']='buy'
            StgyDf.loc[i,'InvestVal']=StgyDf.loc[i-1,'InvestVal']*(1+StgyDf.loc[i,'Ret'])
            print(StgyDf[i-1:i+2])
        elif np.isnan(StgyDf.loc[i,'InvestOp'])==True and StgyDf.loc[i-1,'StrgDecitions']=='buy':
            StgyDf.loc[i,'StrgDecitions']='buy'
            StgyDf.loc[i,'InvestOp']=StgyDf.loc[i-1,'InvestOp']
            StgyDf.loc[i,'InvestVal']=StgyDf.loc[i-1,'InvestVal']*(1+StgyDf.loc[i,'Ret'])
            print(StgyDf[i-1:i+2])
    #print(np.isnan(StgyDf.loc[i,'InvestOp']))
  #Strategy returns calculation
    if np.isnan(StgyDf.loc[i,'InvestOp'])==True:
        StgyDf.loc[i,'StrgRet']=0
    else:
        StgyDf.loc[i,'StrgRet']=StgyDf.loc[i,'InvestVal']/StgyDf.loc[i,'InvestOp']-1
    #buys
    if StgyDf.loc[i,'Signal']==1:
        if DecCount==0:
            StgyDf.loc[i,'StrgDecitions']='buy'
            StgyDf.loc[i,'InvestVal']=1
            StgyDf.loc[i,'InvestOp']=StgyDf.loc[i,'InvestVal']
            StgyDf.loc[i+1,'InvestOp']=StgyDf.loc[i,'InvestVal']
            StgyDf.loc[i,'StrgRet']=StgyDf.loc[i,'InvestVal']/StgyDf.loc[i,'InvestOp']-1
            print(StgyDf[i-1:i+2])
            DecCount+=1
        elif DecCount !=0 and StgyDf.loc[i,'Signal']==1 and StgyDf.loc[i-1,'StrgDecitions']=='sell':
            StgyDf.loc[i,'StrgDecitions']='buy'
            StgyDf.loc[i,'InvestOp']=StgyDf.loc[i-1,'InvestOp']
            StgyDf.loc[i,'InvestVal']=StgyDf.loc[i,'InvestOp']
            StgyDf.loc[i+1,'InvestOp']=StgyDf.loc[i,'InvestVal']
            StgyDf.loc[i+1,'InvestOp']=StgyDf.loc[i,'InvestVal']
            StgyDf.loc[i,'StrgRet']=StgyDf.loc[i,'InvestVal']/StgyDf.loc[i,'InvestOp']-1
            print(StgyDf[i-1:i+2])
            DecCount+=1
            
      #print(Stgy_DF.loc[i-1,'StrgDecitions']=='buy')
    if DecCount>0 and StgyDf.loc[i,'Signal']==-1:
    #sell
        if StgyDf.loc[i-1,'StrgDecitions']=='buy':
            StgyDf.loc[i,'StrgDecitions']='sell'
            StgyDf.loc[i,'InvestOp']=StgyDf.loc[i-1,'InvestOp']
            StgyDf.loc[i,'InvestVal']=StgyDf.loc[i-1,'InvestVal']*(1+StgyDf.loc[i,'Ret'])
            StgyDf.loc[i+1,'InvestOp']=StgyDf.loc[i,'InvestVal']
            StgyDf.loc[i,'StrgRet']=StgyDf.loc[i,'InvestVal']/StgyDf.loc[i,'InvestOp']-1
            print(StgyDf[i-1:i+2])
            DecCount=+1
      
StgyDf['InvestVal'].bfill(inplace=True)
    


