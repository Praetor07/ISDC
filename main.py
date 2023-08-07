# This is a sample Python script.

import numpy as np
import pandas as pd
pd.set_option('display.max_rows', None, 'display.max_columns', None)
import requests
from difflib import SequenceMatcher
import operator
import re
from Table_Visualizer import clean_population_cols
import time


def create_list(input_list, rep, pattern):
    final_list = []
    for string in input_list:
        string = pattern.sub(lambda m: rep[re.escape(m.group(0))], string)
        string = string.strip(",")
        string = re.sub(r'(?<=\d),(?=\d)', '|', string)
        row = [element for element in string.split(',') if element != "***"]
        final_list.append(row)
    return final_list


def request_data(link, table_type):
    response_API = requests.get(link)
    df_list = response_API.text.split('\n')
    col_link = f"https://api.census.gov/data/2021/acs/acs5{table_type}/variables"
    col_response_API = requests.get(col_link)
    col_list = col_response_API.text.split('\n')
    final_df_list = create_list(df_list, rep, pattern)
    final_col_list = create_list(col_list, rep, pattern)
    col_df = pd.DataFrame(final_col_list)
    col_dict = {}
    for x, y in zip(col_df[0], col_df[1]):
        col_dict[x] = y
    df = pd.DataFrame(final_df_list)
    df.columns = final_df_list[0]
    df.drop(index=0, axis=0, inplace=True)
    df.rename(columns=col_dict, inplace=True)
    final_cols = []
    for column in df.columns:
        if column.endswith("A") or column.endswith("M"):
            continue
        final_cols.append(column)
    df = df[final_cols]
    df.replace(to_replace={'-888888888': np.nan,'-666666666.0': np.nan,'-666666666':np.nan,'-999999999': np.nan,'-222222222': np.nan,'-333333333': np.nan,'-555555555':np.nan}, inplace=True)
    df.dropna(axis=1, how='all', inplace=True)
    if "NAME" in df.columns:
        df['NAME'] = df['NAME'].str.replace(".",",", regex= True)
        df['NAME'] = df['NAME'].str.replace(",Illinois", "", regex=True)
    df['State'] = "Illinois"
    #print(df.loc[df['NAME']== 'Adams County'])
    #exit()
    return df


def clean_column_names(col_list: list, table: str) -> list:
    new_col_list =[]
    for column in col_list:
        temp = re.sub('!+','!', column)
        temp =  re.sub(':','', temp)
        temp = re.sub('\|', ',', temp)
        new_col_list.append((temp))
    substring_counts = {}
    matches_list=[]
    for i in range(0, len(new_col_list)):
        for j in range(i + 1, len(new_col_list)):
            string1 = new_col_list[i]
            string2 = new_col_list[j]
            matches = SequenceMatcher(None, string1, string2).get_matching_blocks()
            for match in matches:
                #print(match)
                stri = string1[match.a:match.a + match.size]
                if len(stri) >= 4:
                    if stri not in matches_list:
                        matches_list.append(stri)
    for ele in matches_list:
        substring_counts[ele] = sum(ele in datpoi for datpoi in new_col_list)
    #print(substring_counts)
    max_occurring_substring = max(substring_counts.items(), key=operator.itemgetter(1))[0]
    final_col_list = [re.sub(f'{max_occurring_substring}|!','', temp) for temp in new_col_list]
    for i in range(0, len(final_col_list)):
        if final_col_list[i] == '' and table != 'B01001':
            final_col_list[i] = 'Abs_Total'
    #print(col_list, '\n', final_col_list)
    return final_col_list

def store_dashboard_education(df, key):
    desired_cols = ["diploma", "graduate", "associate", "Bachelor"]
    #print(df.head(5))
    for des in desired_cols:
        temp_list = []
        for col in df.columns:
            if re.search(des, col):
                temp_list.append(col)
        #print(temp_list)
        df[temp_list] = df[temp_list].astype(int)
        df[des] = df[temp_list].sum(axis=1)
    edu_cols = {"diploma" : "Less than high school diploma", "graduate" : "High school graduate", "associate" : "Some college or associate's degree", "Bachelor": "Bachelor's degree or higher"}
    df = df.rename(columns=edu_cols)
    df = df[['Less than high school diploma', 'High school graduate', 'Some college or associate\'s degree','Bachelor\'s degree or higher','NAME', 'State','IL DCEO', 'IDPH', 'IDOT District',
       'IDOT Region', 'IEMA', 'LWIA ', 'IDNR', 'ISBE service Areas',
       'ISBE educational service regions']]
    if key == "Hispanic":
        df['Race'] = "N/A"
        df['Ethnicity'] = key
    else:
        df['Race'] = key
        df['Ethnicity'] = "N/A"
    return df


def store_dashboard_transport(df, key):
    df['Car, Truck or Van'] = df['Car.truck.or van - drove alone'] + df['Car.truck.or van - carpooled']
    df['Taxicab, motorcycle, bicycle or other means'] = df['Taxicab.motorcycle.bicycle.or other means']
    df = df[['Car, Truck or Van', 'Public transportation (excluding taxicab)', 'Walked','Taxicab, motorcycle, bicycle or other means',
             'NAME', 'State', 'IL DCEO', 'IDPH', 'IDOT District',
       'IDOT Region', 'IEMA', 'LWIA ', 'IDNR', 'ISBE service Areas',
       'ISBE educational service regions']]
    if key == "Hispanic":
        df['Race'] = "N/A"
        df['Ethnicity'] = key
    else:
        df['Race'] = key
        df['Ethnicity'] = "N/A"
    return df

def store_dashboard_income(df, key):
    df = df[['Abs_Total', 'Less than $10,000', '$10,000 to $14,999',
       '$15,000 to $19,999', '$20,000 to $24,999', '$25,000 to $29,999',
       '$30,000 to $34,999', '$35,000 to $39,999', '$40,000 to $44,999',
       '$45,000 to $49,999', '$50,000 to $59,999', '$60,000 to $74,999',
       '$75,000 to $99,999', '$100,000 to $124,999', '$125,000 to $149,999',
       '$150,000 to $199,999', '$200,000 or more', 'NAME',
       'State','IL DCEO', 'IDPH', 'IDOT District',
       'IDOT Region', 'IEMA', 'LWIA ', 'IDNR', 'ISBE service Areas',
       'ISBE educational service regions']]
    if key == "Hispanic":
        df['Race'] = "N/A"
        df['Ethnicity'] = key
    else:
        df['Race'] = key
        df['Ethnicity'] = "N/A"
    return df

def store_dashboard_pop(df, key):
    df = df[['NAME','State', 'Gender', '0 to 4 years', '5 to 14 years', '15 to 24 years', '25 to 34 years', '35 to 44 years', '45 to 54 years', '55 to 64 years', '65 to 74 years', '75+ years']]
    #temp_df  = df[['0 to 4 years', '5 to 14 years', '15 to 24 years']]
    if key == "Hispanic":
        df['Race'] = "N/A"
        df['Ethnicity'] = key
    else:
        df['Race'] = key
        df['Ethnicity'] = "No Ethncity defined"
    region_df = pd.read_csv('regions_data.csv')
    region_df[['County Name', 'State']] = region_df['County Name'].str.split(', ', expand=True)
    final_df = df
    counter = 0
    for i in ['IL DCEO', 'IDPH', 'IDOT District',
       'IDOT Region', 'IEMA', 'LWIA ', 'IDNR', 'ISBE service Areas',
       'ISBE educational service regions']:
        temp_df = region_df[[i, 'County Name']]
        df['State Agency'] = i
        temp_df2 = df.merge(temp_df, left_on='NAME', right_on='County Name')
        temp_df2 = temp_df2.rename(columns = {i:'Regions'})
        final_df = final_df.append(temp_df2)
    return final_df

def clean_population_race(df):
    df[['Under 5 years', '5 to 9 years', '10 to 14 years','15 to 17 years', '18 and 19 years',
             '20 to 24 years', '25 to 29 years', '30 to 34 years', '35 to 44 years', '45 to 54 years', '55 to 64 years',
             '75 to 84 years', '85 years and over']] = df[['Under 5 years', '5 to 9 years', '10 to 14 years','15 to 17 years', '18 and 19 years',
             '20 to 24 years', '25 to 29 years', '30 to 34 years', '35 to 44 years', '45 to 54 years', '55 to 64 years',
             '75 to 84 years', '85 years and over']].astype('int')
    df['0 to 4 years'] = df['Under 5 years']
    df['5 to 14 years'] = df['5 to 9 years'] + df['10 to 14 years']
    df['15 to 24 years'] = df['15 to 17 years'] + df['18 and 19 years'] + df['20 to 24 years']
    df['25 to 34 years'] = df['25 to 29 years'] + df['30 to 34 years']
    df['75+ years'] = df['75 to 84 years'] + df['85 years and over']
    df.drop(['Under 5 years', '5 to 9 years', '10 to 14 years','15 to 17 years', '18 and 19 years',
             '20 to 24 years', '25 to 29 years', '30 to 34 years',
             '75 to 84 years', '85 years and over'], axis=1, inplace=True)
    return df

def merge_regions_data(df):
    region_df = pd.read_csv('regions_data.csv')
    region_df[['County Name','State']] = region_df['County Name'].str.split(', ', expand=True)
    region_df.drop(['EDR (Same as IL DCEO)', 'State'], axis=1, inplace=True)
    df = df.merge(region_df, left_on='NAME', right_on='County Name')
    return df
    #df = df.merge(region_df, on = )

def clean_population_frame(df: pd.DataFrame) -> pd.DataFrame:
    col_list = df.columns
    df.columns = clean_column_names(col_list, 'B01001')
    df['Gender'] = ''
    male_cols, female_cols, final_cols, transformed_cols = [], [], {}, []
    for col in df.columns:
        if not re.search('Male|Female', col):
            transformed_cols.append(col)
    #blank column is the total estimate, gets trimmed since its part of majority of all other columns
    for column in df.columns:
        if re.search('Male|Female', column):
            sea = re.search('Male|Female', column)
            key_ = column[sea.start():sea.end()]
            if key_ in final_cols:
                final_cols[key_].append(column)
            else:
                final_cols[key_] = transformed_cols.copy()
                final_cols[key_].append(column)
    counter = 0
    transformed_df = pd.DataFrame(columns=final_cols['Male'])
    for county in df['NAME'].unique():
        if counter != 0:
            transformed_df.columns = final_cols["Male"]
        transformed_df = pd.concat([transformed_df, df.loc[df['NAME']== county, final_cols['Male']]], ignore_index=True)
        transformed_df.loc[counter, "Gender"] = "Male"
        counter += 1
        transformed_df.columns = final_cols['Female']
        transformed_df = pd.concat([transformed_df, df.loc[df['NAME']== county, final_cols['Female']]], ignore_index=True)
        transformed_df.loc[counter, 'Gender'] = "Female"
        counter += 1
    final_cols = transformed_cols
    for col in transformed_df.columns:
        if re.search('Male|Female', col):
            sea = re.search('Female', col)
            temp_str = col[sea.end():]
            if temp_str == '':
                temp_str = 'Total'
            final_cols.append(temp_str)
    transformed_df.columns = final_cols
    transformed_df = clean_population_race(transformed_df)
    #print(transformed_df.head(5))
    #transformed_df.drop([''], axis=1, inplace=True)
    return transformed_df


if __name__ == '__main__':
    rep = {'"': '', '[': '', ']': '', ', ': '.'}
    rep_cols = {'"': '', '[': '', ']': ''}
    #table_dict = {'S1501':'Educational_attainment', 'S1601': 'Languages', 'C08301':'Vehicles', 'S2401': 'Occupation', 'S2404' : 'Industry' ,'S0101': 'Population_by_age', 'B02001' : 'Population_by_race', 'B03003' : 'Population_by_ethnicity', 'S1901' : 'Household_income' , 'S1701' : 'Poverty_Status', 'S1501' : 'Educational_Attainment', 'C24050' : 'Major_occupations' ,'B08201' : 'Vehicle_count','B25002':'Housing_Tenure', 'B25003' : 'Housing_rent','S2506' :'Housing_affordability', 'DP04' : 'Housing_affordability_1', 'B25077' : 'Housing_affordability_2'}
    table_dict = {'B01001A': 'White(alone)', 'B01001B': 'Black(alone)', 'B01001C': 'AIAN(alone)', 'B01001D': 'Asian(alone)', 'B01001E' : 'NHPI(alone)', 'B01001F' : 'Other race alone', 'B01001G' : '2 or more races', 'B01001I': 'Hispanic'}
    #table_dict = {'C15002A': 'White(alone)', 'C15002B': 'Black(alone)', 'C15002C': 'AIAN(alone)', 'C15002D': 'Asian(alone)', 'C15002E' : 'NHPI(alone)', 'C15002F' : 'Other race alone', 'C15002G' : '2 or more races', 'C15002I': 'Hispanic'}
    #table_dict = {'B08105A': 'White(alone)', 'B08105B': 'Black(alone)', 'B08105C': 'AIAN(alone)', 'B08105D': 'Asian(alone)', 'B08105E' : 'NHPI(alone)', 'B08105F' : 'Other race alone', 'B08105G' : '2 or more races', 'B08105I': 'Hispanic'}
    #table_dict = {'B19001A': 'White(alone)', 'B19001B': 'Black(alone)', 'B19001C': 'AIAN(alone)', 'B19001D': 'Asian(alone)', 'B19001E' : 'NHPI(alone)', 'B19001F' : 'Other race alone', 'B19001G' : '2 or more races', 'B19001I': 'Hispanic'}
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    pattern_cols = re.compile("|".join(rep_cols.keys()))
    with open("table_names.txt", "r") as f:
        table = f.readline().strip()
        while table:
            if table.startswith("B") or table.startswith("C"):
                table_type = ''
            elif table.startswith("D"):
                table_type = '/profile'
            else:
                table_type = '/subject'
            state_link = f'https://api.census.gov/data/2021/acs/acs5{table_type}?get=group({table})&for=state:17'
            county_link = f'https://api.census.gov/data/2021/acs/acs5{table_type}?get=group({table})&for=county:*&in=state:17'
            tract_link = f'https://api.census.gov/data/2021/acs/acs5{table_type}?get=group({table})&for=tract:*&in=state:17'
            links_dict = {'county': county_link}
            for link in links_dict:
                printing_df = request_data(links_dict[link], table_type)
                if len(printing_df) < 10 and link != "state":
                    print(f"{link} for {table} is empty")
                    continue
                if table not in table_dict: #need to improve flag logic for population dataframe
                    printing_df.columns = clean_column_names(printing_df.columns, table)
                if table in table_dict:
                    printing_df = clean_population_frame(printing_df)
                        #printing_df.columns = clean_column_names(printing_df.columns)
                    #print(printing_df.head(5))
                    #exit()
                printing_df.to_csv(f"./Data/{table_dict[table]}_{link}.csv")
            table = f.readline().strip()
    pop_dashboard_df = pd.DataFrame()
    for t in table_dict:
        df = pd.read_csv(f"./Data/{table_dict[t]}_county.csv")
        #df = merge_regions_data(df)
        df = store_dashboard_pop(df.copy(), table_dict[t])
        pop_dashboard_df = pd.concat([pop_dashboard_df, df], axis = 0)
    pop_dashboard_df.to_csv("Dashboard.csv")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
