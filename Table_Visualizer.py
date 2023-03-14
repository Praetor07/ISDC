import re
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
pd.set_option('display.max_rows', None, 'display.max_columns', None)

font = "Times New Roman"


def education_att(county_name):
    edu_df = pd.read_csv('./Data/Educational_Attainment_county.csv')
    edu_df = edu_df[edu_df['NAME'] == county_name]
    #Categories: Less than high school; High school graduate; Some college no degree, associate degree; Bachelors; Graduate professional
    cols = [col for col in edu_df if re.search('EstimateTotalAGE BY EDUCAL ATTAINMENT', col)]
    edu_df = edu_df[cols]
    cols = [col for col in edu_df if re.search('Population 25 years and over', col)]
    edu_df = edu_df[cols]
    finals_cols = [re.sub('EstimateTotalAGE BY EDUCAL ATTAINMENT|Population 25 years and over', '', col) for col in edu_df ]
    edu_df.columns = finals_cols
    edu_df = edu_df[edu_df.columns[1:8]]
    edu_df['Less than High School'] = edu_df['Less than 9th grade'] + edu_df['9th to 12th grade.no diploma']
    edu_df.drop(edu_df.columns[:2],inplace = True,axis =1)
    edu_df.columns = ['High School Graduate', 'Some college, no degree', 'Associate\'s degree','Bachelor\'s Degree', 'Graduate or Professional degree', 'Less than High school']
    edu_df = edu_df[['Less than High school', 'High School Graduate', 'Some college, no degree', 'Associate\'s degree','Bachelor\'s Degree', 'Graduate or Professional degree']]
    edu_df = edu_df.T.reset_index()
    edu_df.columns = ['Edu_level','Total']
    light_orange = (1.0, 0.8, 0.64)
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.set_style('darkgrid')
    total = sum(edu_df['Total'])
    ax = sns.barplot(x=edu_df['Total'], y=edu_df['Edu_level'], orient='h', color=light_orange, width=0.6)
    ax.bar_label(ax.containers[0], fontsize=40)
    plt.box(False)
    ax.set_xlabel('', visible=False)
    ax.tick_params(axis='y', which='major', labelsize=50)
    ax.tick_params(axis='x', which='major', labelsize=40)
    plt.yticks(fontname=font)
    ax.set_ylabel('', visible=False)
    plt.rc('axes', labelsize=5)
    plt.xticks(list(range(0, total - 5, total // 4)), [str(x) + '%' for x in list(range(0, 80, 20))])
    plt.savefig(f'./Visualizations/{county_name}_education.png', dpi=300, bbox_inches='tight')

education_att('Champaign County')

def commute(county_name):
    county_name = county_name + ", Illinois"
    commute_df = pd.read_csv('./Data/ori_des.csv')
    incoming_df = commute_df[(commute_df['w_county_name'] == county_name) & (commute_df['h_county_name'] != county_name)]
    outgoing_df = commute_df[(commute_df['w_county_name'] != county_name) & (commute_df['h_county_name'] == county_name)]
    inplace_df = commute_df[(commute_df['w_county_name'] == county_name) & (commute_df['h_county_name'] == county_name)]
    metrics =[[incoming_df['S000'].sum(), outgoing_df['S000'].sum(), inplace_df['S000'].sum()]]
    columns = ['Live outside county, commute in for work', 'Live and work in county', 'Live inside county, commute outside for work']
    #columns = [re.sub("(.{28})", "\\1\n", label, 0, re.DOTALL) for label in columns]
    com_df = pd.DataFrame(metrics, columns=columns)
    return com_df

commute('Champaign County')

def mode_travel(county_name):
    travel_df = pd.read_csv('./Data/Vehicles_county.csv')
    travel_df = travel_df[travel_df['NAME'] == county_name]
    travel_df['Taxicab,motorcyle,bicycle or other means'] = travel_df['Taxicab'] + travel_df['Motorcycle'] + travel_df['Bicycle'] + travel_df['Other means']
    travel_df = travel_df[['Car.truck.or van', 'Public transportation (excluding taxicab)', 'Walked', 'Taxicab,motorcyle,bicycle or other means']]
    travel_df.columns =['Car,truck,or van', 'Public transportation', 'Walked', 'Taxicab,motorcyle,bicycle or other means']
    travel_df = travel_df.T.reset_index()
    travel_df.columns = ['Vehicle', 'Total']
    light_orange = (1.0, 0.8, 0.64)
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.set_style('darkgrid')
    total = sum(travel_df['Total'])
    ax = sns.barplot(x=travel_df['Total'], y=travel_df['Vehicle'], orient='h', color=light_orange, width=0.6)
    ax.bar_label(ax.containers[0], fontsize=40)
    plt.box(False)
    ax.set_xlabel('', visible=False)
    ax.tick_params(axis='y', which='major', labelsize=50)
    ax.tick_params(axis='x', which='major', labelsize=40)
    xlabels_new = [re.sub("(.{25})", "\\1\n", label, 0, re.DOTALL) for label in travel_df['Vehicle']]
    plt.yticks(range(4), xlabels_new, fontname=font)
    plt.yticks(fontname=font)
    ax.set_ylabel('', visible=False)
    plt.rc('axes', labelsize=5)
    plt.xticks(list(range(0, total - 5, total // 4)), [str(x) + '%' for x in list(range(0, 80, 20))])
    plt.savefig(f'./Visualizations/{county_name}_vehicle.png', dpi=300, bbox_inches='tight')


mode_travel('Champaign County')

def occupation(county_name):
    occ_df = pd.read_csv('./Data/Occupation_county.csv')
    occ_df = occ_df[occ_df['NAME'] == county_name]
    occ_df.columns = [re.sub('TotalCivilian employed population 16 years and over' ,'', i) for i in occ_df.columns]
    col_list = ['Management.business.science.and arts occupations', 'Service occupations' ,'Sales and office occupations', 'Natural resources.construction.and maintenance occupations', 'Production.transportation.and material moving occupations']
    occ_df = occ_df[col_list]
    finalcols = ['Management, science and related', 'Services', 'Sales and office', 'Natural Resources and maintenance', 'Production and Transportation']
    occ_df.columns = finalcols
    occ_df = occ_df.T.reset_index()
    occ_df.columns = ['Occupation', 'Total']
    light_orange = (1.0, 0.8, 0.64)
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.set_style('darkgrid')
    total = sum(occ_df['Total'])
    ax = sns.barplot(x=occ_df['Total'], y=occ_df['Occupation'], orient='h', color=light_orange, width=0.6)
    ax.bar_label(ax.containers[0], fontsize=40)
    plt.box(False)
    ax.set_xlabel('', visible=False)
    ax.tick_params(axis='y', which='major', labelsize=50)
    ax.tick_params(axis='x', which='major', labelsize=40)
    plt.yticks(fontname=font)
    ax.set_ylabel('', visible=False)
    plt.rc('axes', labelsize=5)
    plt.xticks(list(range(0, total-5, total // 4)), [str(x) + '%' for x in list(range(0, 80, 20))])
    plt.savefig(f'./Visualizations/{county_name}_occupation.png', dpi=300, bbox_inches='tight')

occupation('Champaign County')


def industry(county_name):
    industry_df = pd.read_csv('./Data/Industry_county.csv')
    industry_df = industry_df[industry_df['NAME'] == county_name]
    industry_df.columns = [re.sub('TotalFull-time.year-round civilian employed population 16 years and over', '', col) for col in industry_df.columns]
    cols = ['Agriculture.forestry.fishing and hunting.and mining' ,'Construction', 'Manufacturing', 'Wholesale trade', 'Retail trade', 'Transportation and warehousing.and utilities', 'Information', 'Finance and insurance.and real estate and rental and leasing', 'Professional.scientific.and management.and administrative and waste management services', 'Educational services.and health care and social assistance', 'Arts.entertainment.and recreation.and accommodation and food services', 'Other services.except public administration','Public administration']
    industry_df = industry_df[cols]
    industry_df.columns = ['Ag, Forestry, Fishing and hunting', 'Construction', 'Manufacturing', 'WholeSale Trade', 'Retail Trade', 'Transport, warehouse and utilities', 'Information', 'Finance,Insurance and Real estate', 'Prof, mgmt and waste mgmt', 'Education,healthcare and social services', 'Arts, entertainment, recreation and food', 'Other service', 'Public Admin']
    industry_df = industry_df.T.reset_index()
    industry_df.columns = ['Industry', 'Total']
    light_orange = (1.0, 0.8, 0.64)
    fig, ax = plt.subplots(figsize=(16, 35))
    sns.set_style('darkgrid')
    total = sum(industry_df['Total'])
    ax = sns.barplot(x=industry_df['Total'], y=industry_df['Industry'], orient='h', color=light_orange, width=0.6)
    ax.bar_label(ax.containers[0], fontsize=45)
    plt.box(False)
    ax.set_xlabel('', visible=False)
    ax.tick_params(axis='y', which='major', labelsize=55)
    ax.tick_params(axis='x', which='major', labelsize=35)
    xlabels_new = [re.sub("(.{21})", "\\1\n", label, 0, re.DOTALL) for label in industry_df['Industry']]
    plt.yticks(range(13), xlabels_new,fontname=font)
    ax.set_ylabel('', visible=False)
    plt.rc('axes', labelsize=5)
    plt.xticks(list(range(0, total//2, total//10)), [str(x) + '%' for x in list(range(0, 50, 10))])
    plt.savefig(f'./Visualizations/{county_name}_industry.png', dpi=300, bbox_inches='tight')

industry('Champaign County')



def vehicle_count(county_name):
    vehicle_df = pd.read_csv('./Data/Vehicle_count_county.csv')
    vehicle_df = vehicle_df[vehicle_df['NAME'] == county_name]
    vehicle_df = vehicle_df[vehicle_df.columns[2:7]].T.reset_index()
    vehicle_df.columns = ['Vehicle_count', 'Total']
    light_orange = (1.0, 0.8, 0.64)
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.set_style('darkgrid')
    total = sum(vehicle_df['Total'])
    ax = sns.barplot(x=vehicle_df['Total'], y=vehicle_df['Vehicle_count'], orient='h', color=light_orange, width=0.6)
    ax.bar_label(ax.containers[0], fontsize=40)
    plt.box(False)
    ax.set_xlabel('', visible=False)
    ax.tick_params(axis='y', which='major', labelsize=50)
    ax.tick_params(axis='x', which='major', labelsize=40)
    plt.yticks(fontname=font)
    ax.set_ylabel('', visible=False)
    plt.rc('axes', labelsize=5)
    plt.xticks(list(range(0, total-20, total//4)), [str(x) + '%' for x in list(range(0, 80, 20))])
    plt.savefig(f'./Visualizations/{county_name}_vehcilecount.png', dpi=300, bbox_inches='tight')

vehicle_count('Champaign County')
def language(county_name):
    lang_df = pd.read_csv('./Data/Languages_county.csv')
    lang_df = lang_df[lang_df['NAME'] == county_name]
    languages_dict = {}
    languages = ['Speak only English', 'Spanish', 'Indo-European languages', 'Asian and Pacific Island languages', 'Other languages']
    lang_regex = '|'.join(languages)
    for col in lang_df.columns:
        if re.search('EstimateTotalPopulation', col):
            if re.search(lang_regex,col):
                l = col[re.search(lang_regex,col).start():re.search(lang_regex,col).end()]
                if l not in languages_dict:
                    languages_dict[l] = []
                languages_dict[l].append(col)
    for lang in languages_dict:
        lang_df[lang] = lang_df[languages_dict[lang]].sum(axis=1)
        lang_df.drop(columns = lang_df[languages_dict[lang]], inplace=True, axis=1)
    lang_df = lang_df[lang_df.columns[-5:]].T.reset_index()
    lang_df.columns = ['Language', 'Total']
    total = sum(lang_df['Total'])
    light_orange = (1.0, 0.8, 0.64)
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.set_style('darkgrid')
    ax = sns.barplot(x=lang_df['Total'], y=lang_df['Language'], orient='h', color=light_orange, width=0.6)
    ax.bar_label(ax.containers[0], fontsize=40)
    plt.box(False)
    ax.set_xlabel('', visible=False)
    ax.tick_params(axis='y', which='major', labelsize=50)
    ax.tick_params(axis='x', which='major', labelsize=40)
    plt.yticks(fontname=font)
    ax.set_ylabel('', visible=False)
    plt.rc('axes', labelsize=5)
    plt.xticks(list(range(0, total-5, total//5)), [str(x) + '%' for x in list(range(0, 100, 20))])
    plt.savefig(f'./Visualizations/{county_name}_languageimage.png', dpi=300, bbox_inches='tight')

language('Champaign County')
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
    fig, ax = plt.subplots(figsize=(45,20))
    x['Male'] = x['Male']*-1
    blue= (0.67,  0.75, 0.90)
    light_orange = (1.0, 0.8, 0.64)
    ax1 = sns.barplot(x='Male', y='Age', data=x, order=age_order, color=blue, lw =0, width=0.6)
    sns.barplot(x='Female', y='Age', data=x, order=age_order, color=light_orange, lw =0, width=0.6)
    ax.tick_params(axis='y', which='major', labelsize=65)
    ax.tick_params(axis='x', which='major', labelsize=50)
    plt.yticks(fontname=font)
    plt.xticks(list(range(-25000,25000,5000)), [str(i) + '%' for i in range(-25,25,5)])
    ax.set_xlabel('', visible=False)
    plt.box(False)
    colors = {'Male': blue, 'Female':  light_orange}
    labels = list(colors.keys())
    handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) for label in labels]
    plt.legend(handles, labels, fontsize=50)
    # set the chart title
    # show the chart
    plt.savefig(f'./Visualizations/{county_name}_PopPyramid2.png')

population_pyramid('Champaign County')

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
        c = c.replace('to', ' - ')
        c = c.replace('HouseholdsTotal', '')
        col_list.append(c)
    income_df.columns = col_list
    income_df = income_df.T.reset_index()
    income_df.columns = ['income', 'percent']
    light_orange = (1.0, 0.8, 0.64)
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.set_style('darkgrid')
    ax = sns.barplot(x=income_df['percent'], y=income_df['income'], orient='h', color=light_orange, width=0.4)
    ax.bar_label(ax.containers[0], fontsize=25)
    plt.box(False)
    ax.set_xlabel('', visible=False)
    ax.tick_params(axis='y', which='major', labelsize=30)
    ax.tick_params(axis='x', which='major', labelsize=30)
    plt.yticks(fontname=font)
    ax.set_ylabel('', visible=False)
    plt.rc('axes', labelsize=5)
    plt.xticks(list(range(0, 40, 10)), [str(x) + '%' for x in list(range(0, 40, 10))])
    plt.savefig(f'./Visualizations/{county_name}_incomeimage.png', dpi=300, bbox_inches='tight')

housing_income('Champaign County')

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
    fig, ax = plt.subplots(figsize=(20,15))
    sns.set_style('darkgrid')
    ax = sns.barplot(x=race_df['Total'], y=race_df['Race'], orient='h', color= light_orange, width=0.6)
    ax.bar_label(ax.containers[0], fontsize=50)
    plt.box(False)
    ax.set_xlabel('', visible=False)
    ax.tick_params(axis='y', which='major', labelsize=65)
    ax.tick_params(axis='x', which='major', labelsize=50)
    plt.yticks(fontname=font)
    ax.set_ylabel('', visible=False)
    plt.rc('axes', labelsize=5)
    plt.xticks(list(range(0,total,int(0.2*total))),[str(x)+'%' for x in list(range(0,110,20))])
    plt.savefig(f'./Visualizations/{county_name}_Raceimage.png', dpi=300, bbox_inches='tight')

population_by_race('Champaign County')

def population_by_ethnicity(county_name):
    eth_df = pd.read_csv('./Data/Population_by_ethnicity_county.csv')
    eth_df = eth_df[eth_df['NAME'] == county_name]
    eth_df = eth_df[['Not Hispanic or Latino', 'Hispanic or Latino']]
    eth_df = eth_df.T.reset_index()
    eth_df.columns = ['Ethnicity', 'Total']
    total = eth_df['Total'].sum()
    eth_df['Percent'] = (eth_df['Total'] / total) * 100
    light_orange = (1.0, 0.8, 0.64)
    fig, ax = plt.subplots(figsize=(11, 5))
    ax = sns.barplot(x=eth_df['Total'], y=eth_df['Ethnicity'], orient='h', color=light_orange, width=0.4)
    ax.bar_label(ax.containers[0], fontsize=35)
    plt.box(False)
    plt.tight_layout()
    ax.set_xlabel('', visible=False)
    ax.tick_params(axis='y', which='major', labelsize=40)
    ax.tick_params(axis='x', which='major', labelsize=35)
    plt.yticks(fontname=font)
    ax.set_ylabel('', visible=False)
    plt.rcParams['font.size'] = 12
    plt.xticks(list(range(0,total,int(0.2*total))), [str(x) + '%' for x in list(range(0, 110, 20))])
    plt.savefig(f'./Visualizations/{county_name}_Ethnicimage.png', dpi=300, bbox_inches='tight')

population_by_ethnicity('Champaign County')
