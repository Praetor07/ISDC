import re
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
pd.set_option('display.max_rows', None, 'display.max_columns', None)


def clean_population_cols(df):
    df['0 to 9 years'] = df['Under 5 years'] + df['5 to 9 years']
    df['10 to 19 years'] = df['10 to 14 years'] + df['15 to 19 years']
    df['20 to 29 years'] = df['20 to 24 years'] + df['25 to 29 years']
    df['30 to 39 years'] = df['30 to 34 years'] + df['35 to 39 years']
    df['40 to 49 years'] = df['40 to 44 years'] + df['45 to 49 years']
    df['50 to 59 years'] = df['50 to 54 years'] + df['55 to 59 years']
    df['60 to 69 years'] = df['60 to 64 years'] + df['65 to 69 years']
    df['70 to 79 years'] = df['70 to 74 years'] + df['75 to 79 years']
    df['80+ years'] = df['80 to 84 years'] + df['85 years and over']
    df.drop(['Under 5 years', '5 to 9 years', '10 to 14 years',
       '15 to 19 years', '20 to 24 years', '25 to 29 years', '30 to 34 years',
       '35 to 39 years', '40 to 44 years', '45 to 49 years', '50 to 54 years',
       '55 to 59 years', '60 to 64 years', '65 to 69 years', '70 to 74 years',
       '75 to 79 years', '80 to 84 years', '85 years and over'], axis=1, inplace=True)
    return df.T

def population_pyramid(county_name):
    pop_df = pd.read_csv('./Data/Population_by_age_county.csv')
    pop_df = pop_df[pop_df['NAME'] == county_name]
    pop_df.columns = [col.replace('TotalTotal population','') for col in pop_df.columns]
    gender_cols = [col for col in pop_df.columns if re.search('Male|Female', col) and not re.search('Percen|SELECTED|SUMMARY', col)]
    pop_df = pop_df[gender_cols]
    dataframe_dict = {'Male': {}, 'Female': {}}
    for col in pop_df.columns:
        if re.search('Male', col):
            temp = re.sub('Male|Total populationAGE','', col)
            dataframe_dict['Male'][temp] = pop_df[col].values.tolist()[0]
        elif re.search('Female', col):
            temp = re.sub('Female|Total populationAGE', '', col)
            dataframe_dict['Female'][temp] = pop_df[col].values.tolist()[0]
    for key in dataframe_dict:
        if key == 'Male':
            x = pd.DataFrame.from_dict(dataframe_dict['Male'], orient='index')
            x.columns = ['Male']
        if key == 'Female':
            y = pd.DataFrame.from_dict(dataframe_dict['Female'], orient='index')
            y.columns = ['Female']
    x = pd.concat([x,y], axis=1)
    x = clean_population_cols(x.T)
    x.reset_index(inplace=True)
    x.columns = ['Age','Male', 'Female']
    x.drop([0],axis=0, inplace=True)
    age_order = list(x['Age'].unique()[::-1])
    fig, ax = plt.subplots(figsize=(20,20))
    x['Male'] = x['Male']*-1
    blue= (0.67,  0.75, 0.90)
    light_orange = (1.0, 0.8, 0.64)
    ax1 = sns.barplot(x='Male', y='Age', data=x, order=age_order, color=blue, lw =0, width=0.4)
    sns.barplot(x='Female', y='Age', data=x, order=age_order, color=light_orange, lw =0, width=0.4)
    ax.tick_params(axis='y', which='major', labelsize=24)
    ax.tick_params(axis='x', which='major', labelsize=24)
    plt.xticks(list(range(-25000,25000,5000)), [str(i) + '%' for i in range(-25,25,5)])
    ax.set_xlabel('', visible=False)
    plt.box(False)
    colors = {'Male': blue, 'Female':  light_orange}
    labels = list(colors.keys())
    handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) for label in labels]
    plt.legend(handles, labels, fontsize=20)
    # set the chart title
    # show the chart
    plt.savefig(f'./Visualizations/{county_name}_PopPyramid2.png')


def housing_rent(county_name):
    rent_df = pd.read_csv('./Data/Housing_rent_county.csv')
    rent_state_df = pd.read_csv('./Data/Housing_rent_state.csv')
    rent_df = rent_df[rent_df['NAME'] == county_name]
    rent_df = rent_df[['Owner occupied', 'Renter occupied']]
    rent_state_df = rent_state_df[['Owner occupied', 'Renter occupied']]
    final_rent_df = pd.concat([rent_df.T,rent_state_df.T], axis=1)
    final_rent_df.reset_index(inplace=True)
    final_rent_df.columns = ['', county_name, 'State']
    return final_rent_df


def housing_income(county_name):
    income_df = pd.read_csv('./Data/Household_income_county.csv')
    income_df = income_df[income_df['NAME'] == county_name]
    income_df = income_df[income_df.columns[4:14]]
    col_list = []
    for c in income_df.columns:
        c = c.replace('|', ',')
        c = c.replace('HouseholdsTotal','')
        col_list.append(c)
    income_df.columns = col_list
    income_df = income_df.T.reset_index()
    income_df.columns = ['income', 'percent']
    light_orange = (1.0, 0.8, 0.64)
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.set_style('darkgrid')
    ax = sns.barplot(x=income_df['percent'], y=income_df['income'], orient='h', color=light_orange, width=0.4)
    ax.bar_label(ax.containers[0], fontsize=20)
    plt.box(False)
    ax.set_xlabel('', visible=False)
    ax.tick_params(axis='y', which='major', labelsize=23)
    ax.tick_params(axis='x', which='major', labelsize=20)
    ax.set_ylabel('', visible=False)
    plt.rc('axes', labelsize=5)
    plt.xticks(list(range(0, 40, 10)), [str(x) + '%' for x in list(range(0, 40, 10))])
    plt.savefig(f'./Visualizations/{county_name}_incomeimage.png', dpi=300, bbox_inches='tight')


def housing_table(county_name):
    housing_county_df = pd.read_csv('./Data/Housing_Tenure_county.csv')
    housing_state_df = pd.read_csv('./Data/Housing_Tenure_state.csv')
    housing_county_df = housing_county_df[housing_county_df['NAME'] == county_name]
    housing_county_df = housing_county_df[['Abs_Total','Occupied','Vacant']]
    housing_state_df = housing_state_df[['Abs_Total','Occupied','Vacant']]
    housing_county_df = pd.concat([housing_county_df, housing_state_df], axis=0)
    housing_county_df.columns = ['Total Housing Units','Occupied', 'Vacant']
    housing_county_df = housing_county_df.T
    housing_county_df.reset_index(inplace=True)
    housing_county_df.columns = ['',county_name, 'State']
    return housing_county_df

def clean_affordability(affordability_df, affordability1_df, affordability2_df):
    col = [
        'Percent owner-occupied housing units with a mortgageOwner-occupied housing units with a mortgageMONTHLY HOUSING COSTSMedian (dollars)',
        'Owner-occupied housing units with a mortgageOwner-occupied housing units with a mortgage']
    col1 = ['EstimateGROSS RENTOccupied paying rentMedian (dollars)',
            'PercentGROSS RENT AS A PERCENTAGE OF HOUSEHOLD INCOME (GRAPI)Occupied paying rent (excluding where GRAPI cannot be computed)35.0 percent or more',
            'PercentGROSS RENT AS A PERCENTAGE OF HOUSEHOLD INCOME (GRAPI)Occupied paying rent (excluding where GRAPI cannot be computed)30.0 to 34.9 percent',
            'PercentSELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)Housing with a mortgage (excluding where SMOCAPI cannot be computed)30.0 to 34.9 percent',
            'PercentSELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI)Housing with a mortgage (excluding where SMOCAPI cannot be computed)35.0 percent or more']
    col2 = ['EstimateMedian value (dollars)']
    affordability_df = affordability_df[col]
    affordability1_df = affordability1_df[col1]
    affordability2_df = affordability2_df[col2]
    affordability_df.columns = ['Median monthly mortgage cost', 'Owner-occupied mortgaged homes']
    affordability1_df.columns = ['Median gross rent, 2021 ($)', 'GRAPI, 30-34', 'GRAPI 35+', 'SMOCAPI, 30-34', 'SMOCAPI 35+']
    affordability1_df['Rent > 30% of household income'] = affordability1_df['GRAPI, 30-34'] + affordability1_df[
        'GRAPI 35+']
    affordability1_df['Cost > 30% of household income'] = affordability1_df['SMOCAPI, 30-34'] + affordability1_df[
        'SMOCAPI 35+']
    affordability1_df.drop(columns=['GRAPI, 30-34', 'GRAPI 35+', 'SMOCAPI, 30-34', 'SMOCAPI 35+'], inplace=True)
    affordability2_df.columns = ['Median House Value($)']
    return affordability_df.T, affordability1_df.T, affordability2_df.T

def housing_affordability(county_name):
    affordability_df = pd.read_csv('./Data/Housing_affordability_county.csv')
    affordability1_df = pd.read_csv('./Data/Housing_affordability_1_county.csv')
    affordability2_df = pd.read_csv('./Data/Housing_affordability_2_county.csv')
    affordability_df = affordability_df[affordability_df['NAME'] == county_name]
    affordability1_df = affordability1_df[affordability1_df['NAME'] == county_name]
    affordability2_df = affordability2_df[affordability2_df['NAME'] == county_name]
    affordability_state_df = pd.read_csv('./Data/Housing_affordability_state.csv')
    affordability1_state_df = pd.read_csv('./Data/Housing_affordability_1_state.csv')
    affordability2_state_df = pd.read_csv('./Data/Housing_affordability_2_state.csv')
    affordability_state_df, affordability1_state_df, affordability2_state_df = clean_affordability(affordability_state_df, affordability1_state_df, affordability2_state_df)
    affordability_df, affordability1_df, affordability2_df = clean_affordability(affordability_df, affordability1_df, affordability2_df)
    county_df = pd.concat([affordability_df,affordability1_df, affordability2_df], axis =0)
    state_df = pd.concat([affordability_state_df, affordability1_state_df, affordability2_state_df], axis=0)
    state_df = pd.concat([county_df, state_df], axis=1)
    state_df.reset_index(inplace=True)
    state_df.columns = ['',county_name, 'State']
    state_df = state_df.round(2)
    return state_df


def population_by_race(county_name):
    race_df = pd.read_csv('./Data/Population_by_race_county.csv')
    race_df = race_df[race_df['NAME'] == county_name]
    race_df = race_df[race_df.columns[2:9]]
    final_col_list = []
    for col in race_df.columns:
        if not re.search('Some',col):
            temp = col.replace('alone', '')
            final_col_list.append(temp.strip())
        else:
            final_col_list.append(col)
    final_col_list[final_col_list.index('Native Hawaiian and Other Pacific Islander')] ='NH and Pacific Islander'
    race_df.columns = final_col_list
    race_df = race_df.T.reset_index()
    race_df.columns = ['Race', 'Total']
    total = race_df['Total'].sum()
    race_df['Percent'] = (race_df['Total']/total)*100
    light_orange = (1.0, 0.8, 0.64)
    fig, ax = plt.subplots(figsize=(15,10))
    sns.set_style('darkgrid')
    ax = sns.barplot(x=race_df['Total'], y=race_df['Race'], orient='h', color= light_orange, width=0.4)
    ax.bar_label(ax.containers[0], fontsize=20)
    plt.box(False)
    ax.set_xlabel('', visible=False)
    ax.tick_params(axis='y', which='major', labelsize=23)
    ax.tick_params(axis='x', which='major', labelsize=20)
    ax.set_ylabel('', visible=False)
    plt.rc('axes', labelsize=5)
    plt.xticks(list(range(0,total,int(0.2*total))),[str(x)+'%' for x in list(range(0,110,20))])
    plt.savefig(f'./Visualizations/{county_name}_Raceimage.png', dpi=300, bbox_inches='tight')


def population_by_ethnicity(county_name):
    eth_df = pd.read_csv('./Data/Population_by_ethnicity_county.csv')
    eth_df = eth_df[eth_df['NAME'] == county_name]
    eth_df = eth_df[['Not Hispanic or Latino', 'Hispanic or Latino']]
    eth_df = eth_df.T.reset_index()
    eth_df.columns = ['Ethnicity', 'Total']
    total = eth_df['Total'].sum()
    eth_df['Percent'] = (eth_df['Total'] / total) * 100
    light_orange = (1.0, 0.8, 0.64)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax = sns.barplot(x=eth_df['Total'], y=eth_df['Ethnicity'], orient='h', color=light_orange, width=0.2)
    ax.bar_label(ax.containers[0], fontsize=20)
    plt.box(False)
    plt.tight_layout()
    ax.set_xlabel('', visible=False)
    ax.tick_params(axis='y', which='major', labelsize=23)
    ax.tick_params(axis='x', which='major', labelsize=20)
    ax.set_ylabel('', visible=False)
    plt.rcParams['font.size'] = 12
    plt.xticks(list(range(0,total,int(0.2*total))), [str(x) + '%' for x in list(range(0, 110, 20))])
    plt.savefig(f'./Visualizations/{county_name}_Ethnicimage.png', dpi=300, bbox_inches='tight')



