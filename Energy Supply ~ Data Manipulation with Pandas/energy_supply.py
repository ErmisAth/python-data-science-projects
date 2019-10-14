import pandas as pd
import numpy as np
import re

def answer_one():

    """
    Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names).
    Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15).
    The index of this DataFrame should be the name of the country, and the columns should be 
    ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 
    'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', 
    '2013', '2014', '2015']
    """

    #read excel, skip header and footer, drop first 2 columns
    energy = pd.read_excel('Energy Indicators.xls', skiprows = 17, skipfooter = 38,  
                parse_cols = range(2,6))
    #rename columns
    energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    #convert petajoules to gigajoules
    energy['Energy Supply'] *= 1000000
    #put NaN in last three columns if their values are non-numeric
    energy.iloc[:,1:4] = energy.iloc[:,1:4][energy.iloc[:,1:4].applymap(np.isreal)]
    #drop digits in country names
    energy['Country'] = energy.apply(lambda x: re.sub('\d', '', x['Country']), axis=1)
    #drop parentheses and the text inside in country names
    energy['Country'] = energy.apply(lambda x: re.sub(' \(([^)]+)\)', '', x['Country']), axis=1)
    #replace certain country names
    energy['Country'].replace('Republic of Korea', 'South Korea', inplace = True)
    energy['Country'].replace('United States of America', 'United States', inplace = True)
    energy['Country'].replace('United Kingdom of Great Britain and Northern Ireland', 'United Kingdom',
                inplace = True)
    energy['Country'].replace('China, Hong Kong Special Administrative Region', 'Hong Kong', inplace = True)
    
    #read csv and skip header
    GDP = pd.read_csv('world_bank.csv', skiprows = 4)
    #replace certain country names
    GDP['Country Name'].replace('Korea, Rep.', 'South Korea', inplace = True)
    GDP['Country Name'].replace('Iran, Islamic Rep.', 'Iran', inplace = True)
    GDP['Country Name'].replace('Hong Kong SAR, China', 'Hong Kong', inplace = True)
    
    #read excel
    ScimEn = pd.read_excel('scimagojr-3.xlsx')
    
    #merge ScimEN and energy
    Joined_df = pd.merge(ScimEn.iloc[0:15].set_index('Country'), energy.set_index('Country'), how = 'inner',
                left_index = True, right_index = True)
    #merge with GDP columns
    Joined_df = Joined_df.merge(GDP[['Country Name', '2006', '2007', '2008', '2009', '2010', '2011', '2012', 
                '2013', '2014', '2015']].set_index('Country Name'), how = 'inner', left_index = True, 
                right_index = True)
    return Joined_df
#print(answer_one())


def answer_two():

    """
    The previous question joined three datasets then reduced this to just the top 15 entries. 
    When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
    """

    #read excel, skip header and footer, drop first 2 columns
    energy = pd.read_excel('Energy Indicators.xls', skiprows = 17, skipfooter = 38,  
                parse_cols = range(2,6))
    #rename columns
    energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    #convert petajoules to gigajoules
    energy['Energy Supply'] *= 1000000
    #put NaN in last three columns if their values are non-numeric
    energy.iloc[:,1:4] = energy.iloc[:,1:4][energy.iloc[:,1:4].applymap(np.isreal)]
    #drop digits in country names
    energy['Country'] = energy.apply(lambda x: re.sub('\d', '', x['Country']), axis=1)
    #drop parentheses and the text inside in country names
    energy['Country'] = energy.apply(lambda x: re.sub(' \(([^)]+)\)', '', x['Country']), axis=1)
    #replace certain country names
    energy['Country'].replace('Republic of Korea', 'South Korea', inplace = True)
    energy['Country'].replace('United States of America', 'United States', inplace = True)
    energy['Country'].replace('United Kingdom of Great Britain and Northern Ireland', 'United Kingdom',
                inplace = True)
    energy['Country'].replace('China, Hong Kong Special Administrative Region', 'Hong Kong', inplace = True)
    #read csv and skip header
    GDP = pd.read_csv('world_bank.csv', skiprows = 4)
    #replace certain country names
    GDP['Country Name'].replace('Korea, Rep.', 'South Korea', inplace = True)
    GDP['Country Name'].replace('Iran, Islamic Rep.', 'Iran', inplace = True)
    GDP['Country Name'].replace('Hong Kong SAR, China', 'Hong Kong', inplace = True)
    #read excel
    ScimEn = pd.read_excel('scimagojr-3.xlsx')
    #merge ScimEN and energy
    Inner_Join = pd.merge(ScimEn.set_index('Country'), energy.set_index('Country'), how = 'inner',
                left_index = True, right_index = True)
    #merge with GDP columns
    Inner_Join = Inner_Join.merge(GDP[['Country Name', '2006', '2007', '2008', '2009', '2010', '2011', '2012', 
                '2013', '2014', '2015']].set_index('Country Name'), how = 'inner', left_index = True, 
                right_index = True)
    Outer_Join = pd.merge(ScimEn.set_index('Country'), energy.set_index('Country'), how = 'outer',
                left_index = True, right_index = True)
    #merge with GDP columns
    Outer_Join = Outer_Join.merge(GDP[['Country Name', '2006', '2007', '2008', '2009', '2010', '2011', '2012', 
                '2013', '2014', '2015']].set_index('Country Name'), how = 'outer', left_index = True, 
                right_index = True)
    return len(Outer_Join) - len(Inner_Join)
#print(answer_two())

def answer_three():

    """
    What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
    """

    Top15 = answer_one()
    rows = ['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
    return Top15.apply(lambda x: np.mean(x[rows]), axis = 1).sort_values(ascending = False).rename('avgGDP')
#print(answer_three())

def answer_four():
    
    """
    By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
    """

    Top15 = answer_one()
    rows = ['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
    Top15['avgGDP'] = Top15.apply(lambda x: np.mean(x[rows]), axis = 1)
    Top15.sort_values('avgGDP', ascending = False, inplace = True)
    return Top15.loc[Top15.iloc[5].name, '2015'] - Top15.loc[Top15.iloc[5].name, '2006']
#print(answer_four())