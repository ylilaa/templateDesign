from template import PricerBase
from pricers import PricerA, PricerB
from data import Bond
from template import PricerBase
import pandas as pd
import pricers
def pricer(pricer : PricerBase,bond : Bond) -> float:
    return pricer.template_method(bond)
    

if __name__=='__main__':
    df_excel = pd.read_excel('Base titres.xlsx' ,decimal=',') # european decimals have , instead of .
    # df_excel[df_excel.columns[0]] = pd.to_datetime(df_excel[df_excel.columns[0]],format='%d/%m/%Y').dt.strftime('%Y-%m-%d') # convert dates to the right format for the pricing function
    # df_excel[df_excel.columns[3]] = pd.to_datetime(df_excel[df_excel.columns[3]],format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
    # df_excel[df_excel.columns[4]] = pd.to_datetime(df_excel[df_excel.columns[4]],format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
    prices = []
    bond_types = []
    for row in df_excel.itertuples():
        bond = Bond(row._4,row._1,row._5,row._9,row._6,row._7)
        prices.append(pricer(getattr(pricers, f'Pricer{bond.type}')(),bond)) 
        bond_types.append(bond.type)
    df_excel['priced'] = prices
    df_excel['types'] = bond_types
    df_excel.to_excel('Base titres_from_template.xlsx', index=False) # pick same file to overwrite content , can use sheet_name= for a specific sheet in the file
