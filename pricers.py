from __future__ import annotations
from data import Bond
from template import PricerBase
import pandas as pd
from datetime import datetime
from utils import get_days_in_year

class PricerA(PricerBase):
    """
    Concrete Pricer, overrides get_valo abstractMethod.
    """
    
    def get_valo(self, bond : Bond) -> float:
        return bond.nominal * ((1+(bond.facial/100)*(bond.mi/360))/(1+(bond.ytm/100)*(bond.mrr/360)))

class PricerB(PricerBase):
    """
    Concrete Pricer, overrides get_valo abstractMethod.
    """
    # A nettoyer
    def get_valo(self, bond : Bond) -> float:
        emission =  bond.emission
        echeance = bond.echeance
        dateValo = bond.dateValo 
        facial = bond.facial
        nominal = bond.nominal
        ytm = bond.ytm
        leap = bond.leap
        
        # Creating the dataframe
        dates = dates[::-1]
        df = pd.DataFrame()
        dates = [d for d in dates if (d-emission).days>=365]
        df['dates'] = dates
        
        # echeance = echeance_str
        df['leap'] = df['dates'].apply(get_days_in_year)
        df.loc[0,'coupon'] = 100000 * facial * (df.loc[0,'dates']-emission).days / (df.loc[0,'leap'] * 100)
        for i in range(len(dates)-1):
            df.loc[i+1,'coupon'] = 100000 * facial * (df.loc[i+1,'dates']-df.loc[i,'dates']).days / (df.loc[i,'leap'] * 100)
        
        df['flux'] = df['coupon']
        df.iloc[-1,3] =( df.iloc[-1,2] + nominal)
        
        ech = df
        ech.reset_index()
        dfValo = pd.DataFrame(columns=['Date','RangJ','RangA','Yield','FluxActu'])
        dfValo['Date'] = ech[ech['dates']> dateValo]['dates']
        dfValo['leap'] = dfValo['Date'].apply(lambda x: x - pd.DateOffset(years=1)).apply(get_days_in_year)
        dfValo['RangJ']= (dfValo['Date'] - dateValo).dt.days
        dfValo.loc[dfValo.index[0],'RangA']= dfValo.loc[dfValo.index[0],'RangJ'] / 360
        for i in range(dfValo.index[0],len(dfValo.index)+dfValo.index[0]-1):
            dfValo.loc[i+1,'RangA']= dfValo.loc[i,'RangA'] + 1
        dfValo['Yield']= ytm / 100
        dfValo['FluxActu']= ech[ech['dates']> dateValo]['flux'] / (1 + dfValo['Yield'])  ** dfValo['RangA']
        Valo = dfValo['FluxActu'].sum() 
        return Valo


class PricerC(PricerBase):
    """
    Concrete Pricer, overrides get_valo abstractMethod.
    """
    # A nettoyer
    def get_valo(self, bond : Bond) -> float:
        emission =  bond.emission
        echeance = bond.echeance
        dateValo = bond.dateValo 
        facial = bond.facial
        nominal = bond.nominal
        ytm = bond.ytm
        leap = bond.leap
        
        # Creating the dataframe
        dates = bond.dates[::-1]
        df = pd.DataFrame()
        dates = [d for d in dates if (d-emission).days>=365]
        df['dates'] = dates
        
        # echeance = echeance_str
        df['leap'] = df['dates'].apply(get_days_in_year)
        df.loc[0,'coupon'] = 100000 * facial * (df.loc[0,'dates']-emission).days / (df.loc[0,'leap'] * 100)
        for i in range(len(dates)-1):
            df.loc[i+1,'coupon'] = 100000 * facial * (df.loc[i+1,'dates']-df.loc[i,'dates']).days / (df.loc[i,'leap'] * 100)
        
        df['flux'] = df['coupon']
        df.iloc[-1,3] =( df.iloc[-1,2] + nominal)
        
        ech = df
        ech.reset_index()
        dfValo = pd.DataFrame(columns=['Date','RangJ','RangA','Yield','FluxActu'])
        dfValo['Date'] = ech[ech['dates']> dateValo]['dates']
        dfValo['leap'] = dfValo['Date'].apply(lambda x: x - pd.DateOffset(years=1)).apply(get_days_in_year)
        dfValo['RangJ']= (dfValo['Date'] - dateValo).dt.days
        dfValo.loc[dfValo.index[0],'RangA']= dfValo.loc[dfValo.index[0],'RangJ'] / leap
        for i in range(dfValo.index[0],len(dfValo.index)+dfValo.index[0]-1):
            dfValo.loc[i+1,'RangA']= dfValo.loc[i,'RangA'] + 1
        dfValo['Yield']= ytm / 100
        dfValo['FluxActu']= ech[ech['dates']> dateValo]['flux'] / (1 + dfValo['Yield'])  ** dfValo['RangA']
        Valo = dfValo['FluxActu'].sum() 
        return Valo
    
class PricerD(PricerBase):
    """
    Concrete Pricer, overrides get_valo abstractMethod.
    """

    def get_valo(self, bond : Bond) -> float:
        return bond.nominal * ((1+(bond.facial/100)*(bond.mi/bond.leap))/(1+(bond.ytm/100)*(bond.mrr/360)))
        
class PricerE(PricerBase):
    """
    Concrete Pricer, overrides get_valo abstractMethod.
    """

    def get_valo(self, bond : Bond) -> float:
        return bond.nominal * ((1+bond.facial/100)/(1+(bond.ytm/100)*bond.mrr/360))
        
