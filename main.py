# This is a sample Python script.

import numpy as np
import pandas as pd
pd.set_option('display.max_rows', None, 'display.max_columns', None)
import requests
from difflib import SequenceMatcher
import operator
import re
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
    return df


def clean_column_names(col_list: list, table: str) -> list:
    new_col_list =[]
    for column in col_list:
        temp = re.sub('!+','!', column)
        temp =  re.sub(':','', temp)
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
    max_occurring_substring = max(substring_counts.items(), key=operator.itemgetter(1))[0]
    final_col_list = [re.sub(f'{max_occurring_substring}|!','', temp) for temp in new_col_list]
    for i in range(0, len(final_col_list)):
        if final_col_list[i] == '' and table != 'B01001':
            final_col_list[i] = 'Abs_Total'
    #print(col_list, '\n', final_col_list)
    return final_col_list

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
    transformed_df.drop([''], axis=1, inplace=True)
    return transformed_df


if __name__ == '__main__':
    rep = {'"': '', '[': '', ']': '', ', ': '.'}
    rep_cols = {'"': '', '[': '', ']': ''}
    table_dict = {'S1501':'Educational_attainment', 'S1601': 'Languages', 'C08301':'Vehicles', 'S2401': 'Occupation', 'S2404' : 'Industry' ,'S0101': 'Population_by_age', 'B02001' : 'Population_by_race', 'B03003' : 'Population_by_ethnicity', 'S1901' : 'Household_income' , 'S1701' : 'Poverty_Status', 'S1501' : 'Educational_Attainment', 'C24050' : 'Major_occupations' ,'B08201' : 'Vehicle_count','B25002':'Housing_Tenure', 'B25003' : 'Housing_rent','S2506' :'Housing_affordability', 'DP04' : 'Housing_affordability_1', 'B25077' : 'Housing_affordability_2'}
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
            links_dict = {'tract': tract_link, 'county': county_link, 'state': state_link}
            for link in links_dict:
                printing_df = request_data(links_dict[link], table_type)
                if len(printing_df) < 10 and link != "state":
                    print(f"{link} for {table} is empty")
                    continue
                if table not in ['B01001']:
                    printing_df.columns = clean_column_names(printing_df.columns, table)
                if table in ['B01001']:
                    printing_df = clean_population_frame(printing_df)
                        #printing_df.columns = clean_column_names(printing_df.columns)
                    #print(printing_df.head(5))
                    #exit()
                printing_df.to_csv(f"./Data/{table_dict[table]}_{link}.csv")
            table = f.readline().strip()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
