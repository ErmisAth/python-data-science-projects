import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

pd.options.mode.chained_assignment = None  # turn off warning messages

# Dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 
  'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 
  'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 
  'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 
  'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 
  'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 
  'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 
  'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 
  'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 
  'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 
  'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 
  'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 
  'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 
  'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 
  'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 
  'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 
  'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 
  'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 
  'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

import re

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    with open('university_towns.txt', 'r') as file:
        raw_data = file.read()
    raw_data = raw_data.split('\n')
    raw_data.pop()
    
    uni_towns = pd.DataFrame(columns = ['State', 'RegionName'])
    for i in raw_data:
        if '[edit]' in i:
            current_state_name = i.replace('[edit]', '')
            continue
        uni_towns = uni_towns.append({'State': current_state_name, 'RegionName': i}, ignore_index = True)
        uni_towns['RegionName'] = uni_towns.apply(lambda x: re.sub(' \(.*', '', x['RegionName']), axis=1)
        
    return uni_towns
#print(get_list_of_university_towns())

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    
    gdp = pd.read_excel('gdplev.xls', skiprows = 219, names = ['quarters', 'billions'], parse_cols = [4,6])
    gdp['billions'].astype(np.float64, copy = True)
    gdp['differences'] = gdp['billions'].diff()
    
    recession_start = None
    for i in np.arange(1, len(gdp) - 1):
        if (gdp.loc[i, 'differences'] < 0) and (gdp.loc[i + 1, 'differences'] < 0):
            recession_start = gdp.loc[i, 'quarters']
            break
    return recession_start
#print(get_recession_start())

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    
    gdp = pd.read_excel('gdplev.xls', skiprows = 219, names = ['quarters', 'billions'], parse_cols = [4,6])
    gdp['billions'].astype(np.float64, copy = True)
    gdp['differences'] = gdp['billions'].diff()
    
    recession_start = None
    for i in np.arange(1, len(gdp) - 1):
        if (gdp.loc[i, 'differences'] < 0) and (gdp.loc[i + 1, 'differences'] < 0):
            recession_start = i
            break
    recession_end = None
    for i in np.arange(recession_start, len(gdp) - 1):
        if (gdp.loc[i, 'differences'] > 0) and (gdp.loc[i + 1, 'differences'] > 0):
            recession_end = gdp.loc[i + 1, 'quarters']
            break
    return recession_end
#print(get_recession_end())

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    
    gdp = pd.read_excel('gdplev.xls', skiprows = 219, names = ['quarters', 'billions'], parse_cols = [4,6])
    gdp['billions'].astype(np.float64, copy = True)
    gdp['differences'] = gdp['billions'].diff()
    
    recession_start = None
    for i in np.arange(1, len(gdp) - 1):
        if (gdp.loc[i, 'differences'] < 0) and (gdp.loc[i + 1, 'differences'] < 0):
            recession_start = i
            break
    recession_end = None
    for i in np.arange(recession_start, len(gdp) - 1):
        if (gdp.loc[i, 'differences'] > 0) and (gdp.loc[i + 1, 'differences'] > 0):
            recession_end = i
            break
    recession_bottom = np.argmin(gdp.loc[recession_start:recession_end, 'billions'])
    return gdp.loc[recession_bottom, 'quarters']
#print(get_recession_bottom())

def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    
    housing = pd.read_csv('City_Zhvi_AllHomes.csv')#read csv
    housing.drop(housing.columns[housing.columns < '2000'], axis = 1, inplace = True)#drop early dates
    housing.drop(['RegionID', 'Metro', 'CountyName', 'SizeRank'], axis = 1, inplace = True)#drop some columns
    housing['State'] = housing.apply(lambda x: x['State'].replace(x['State'], states[x['State']]), axis=1)#replace acronyms
    housing.set_index(['State', 'RegionName'], inplace = True)#set new index
    housing.columns = pd.PeriodIndex(housing.columns, freq = 'q')#convert strings of dates to quarterly time periods
    housing = housing.groupby(housing.columns, axis = 1).mean()#group same quarters together and calculate mean for group
    return housing
#print(convert_housing_data_to_quarters())

def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    housing_prices = convert_housing_data_to_quarters()
    uni_towns = get_list_of_university_towns()
    recession_start = get_recession_start()
    recession_bottom = get_recession_bottom()
    price_growth = pd.DataFrame(housing_prices[recession_bottom] - housing_prices[recession_start]).copy()
    price_growth.columns = ['growth']
    
    uni_towns_price_growth = price_growth.merge(uni_towns.set_index(['State', 'RegionName']), how = 'inner', 
                                                                         left_index = True, right_index = True)
    uni_towns_price_growth.dropna(inplace = True)
    non_uni_towns_price_growth = price_growth.drop(uni_towns.set_index(['State', 'RegionName']).index)
    non_uni_towns_price_growth.dropna(inplace = True)
    statistic, pvalue = ttest_ind(uni_towns_price_growth['growth'], non_uni_towns_price_growth['growth'])
    if pvalue < 0.01:
        if statistic > 0:
            return (True, pvalue, 'university town')
        else:
            return (True, pvalue, 'non-university town')
    else:
        if statistic > 0:
            return (False, pvalue, 'university town')
        else:
            return (False, pvalue, 'non-university town')
        
#print(run_ttest())