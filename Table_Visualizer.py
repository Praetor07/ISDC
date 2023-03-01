import re
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
pd.set_option('display.max_rows', None, 'display.max_columns', None)


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
    affordability1_df.columns = ['Median gross rent', 'GRAPI, 30-34', 'GRAPI 35+', 'SMOCAPI, 30-34', 'SMOCAPI 35+']
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

housing_affordability('Champaign County')

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
    plt.savefig('Raceimage.png', dpi=300, bbox_inches='tight')


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
    #plt.margins(y=1, tight=True)
    plt.tight_layout()
    ax.set_xlabel('', visible=False)
    ax.tick_params(axis='y', which='major', labelsize=23)
    ax.tick_params(axis='x', which='major', labelsize=20)
    ax.set_ylabel('', visible=False)
    #ax.legend(fontsize=25)
    #plt.rc('axes', labelsize=5)
    plt.rcParams['font.size'] = 12
    plt.xticks(list(range(0,total,int(0.2*total))), [str(x) + '%' for x in list(range(0, 110, 20))])
    plt.savefig('Ethnicimage.png', dpi=300, bbox_inches='tight')


#population_by_ethnicity('Champaign County')



