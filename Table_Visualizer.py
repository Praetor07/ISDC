import re
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
pd.set_option('display.max_rows', None, 'display.max_columns', None)

font = "Times New Roman"


def education_preproc(edu_df):
    cols = [col for col in edu_df if re.search('EstimateTotalAGE BY EDUCAL ATTAINMENT', col)]
    edu_df = edu_df[cols]
    cols = [col for col in edu_df if re.search('Population 25 years and over', col)]
    edu_df = edu_df[cols]
    finals_cols = [re.sub('EstimateTotalAGE BY EDUCAL ATTAINMENT|Population 25 years and over', '', col) for col in
                   edu_df]
    edu_df.columns = finals_cols
    edu_df = edu_df[edu_df.columns[1:8]]
    edu_df['Less than High School'] = edu_df['Less than 9th grade'] + edu_df['9th to 12th grade.no diploma']
    edu_df.drop(edu_df.columns[:2], inplace=True, axis=1)
    edu_df.columns = ['High School Graduate', 'Some college, no degree', 'Associate\'s degree', 'Bachelor\'s Degree',
                      'Graduate or Professional degree', 'Less than High school']
    edu_df = edu_df[['Less than High school', 'High School Graduate', 'Some college, no degree', 'Associate\'s degree',
                     'Bachelor\'s Degree', 'Graduate or Professional degree']]
    edu_df = edu_df.T.reset_index()
    edu_df.columns = ['Edu_level', 'Total']
    return edu_df

def education_att(county_name, label_type=0):
    edu_df = pd.read_csv('./Data/Educational_Attainment_county.csv')
    edu_df_state = pd.read_csv('./Data/Educational_Attainment_state.csv')
    edu_df = edu_df[edu_df['NAME'] == county_name]
    edu_df = education_preproc(edu_df)
    edu_df_state = education_preproc(edu_df_state)
    if label_type == 1:
        edu_bach = edu_df[edu_df['Edu_level'].isin(["Bachelor's Degree","Graduate or Professional degree"])]['Total'].sum()/edu_df['Total'].sum()
        edu_bach_state = edu_df_state[edu_df_state['Edu_level'].isin(["Bachelor's Degree","Graduate or Professional degree"])]['Total'].sum()/edu_df_state['Total'].sum()
        return round(edu_bach,2)*100, round(edu_bach_state, 2)*100
    light_orange = (1.0, 0.6, 0.0)
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.set_style('darkgrid')
    total = sum(edu_df['Total'])
    state_total = sum(edu_df_state['Total'])
    targets = {x: ((y / state_total)) * total for x, y in
               zip(edu_df_state['Edu_level'], edu_df_state['Total'])}
    sns.barplot(x=len(edu_df['Total']) * [total], y=edu_df['Edu_level'], orient='h', color='white',
                width=0.6)
    sns.barplot(x=edu_df['Total'], y=edu_df['Edu_level'], orient='h', color=light_orange, width=0.6)
    # sns.barplot(x=len(race_df['Total'])*[total], y=race_df['Race'], orient='h', color= 'white', width=0.6)
    x, ymins, ymaxs = list(
        zip(*[(targets[v.get_text()], v.get_position()[1] - 0.6 / 2, v.get_position()[1] + 0.6 / 2) for v in
              ax.get_yticklabels()]))
    ax.vlines(x=x, color='black', linestyle='-', linewidth=5, capstyle='butt', ymin=ymins, ymax=ymaxs)
    plot_labels = [f"{x:,}" for x in list(edu_df['Total'])]
    ax.bar_label(ax.containers[0], labels=plot_labels, fontsize=37, label_type='edge', padding=10)
    plt.box(False)
    ax.set_xlabel('', visible=False)
    ax.tick_params(axis='y', which='major', labelsize=50)
    ax.tick_params(axis='x', which='major', labelsize=40)
    plt.yticks(fontname=font)
    ax.set_ylabel('', visible=False)
    plt.rc('axes', labelsize=5)
    plt.xticks(list(range(0, total + 5, total // 5)), [str(x) + '%' for x in list(range(0, 101, 20))])
    plt.savefig(f'./Visualizations/{county_name}_education.png', dpi=300, bbox_inches='tight')

education_att('Champaign County',1)

def commute(county_name):
    county_name = county_name + ", Illinois"
    commute_df = pd.read_csv('./Data/ori_des.csv')
    incoming_df = commute_df[(commute_df['w_county_name'] == county_name) & (commute_df['h_county_name'] != county_name)]
    outgoing_df = commute_df[(commute_df['w_county_name'] != county_name) & (commute_df['h_county_name'] == county_name)]
    inplace_df = commute_df[(commute_df['w_county_name'] == county_name) & (commute_df['h_county_name'] == county_name)]
    metrics =[[incoming_df['S000'].sum(), outgoing_df['S000'].sum(), inplace_df['S000'].sum()]]
    columns = ['Live outside county\n commute in for work',  'Live inside county\n commute outside for work', 'Live and work in county']
    #columns = [re.sub("(.{28})", "\\1\n", label, 0, re.DOTALL) for label in columns]
    com_df = pd.DataFrame(metrics, columns=columns)
    return com_df

commute('Champaign County')

def mode_travel_preproc(travel_df):
    travel_df['Taxicab,motorcyle,bicycle or other means'] = travel_df['Taxicab'] + travel_df['Motorcycle'] + travel_df[
        'Bicycle'] + travel_df['Other means']
    travel_df = travel_df[['Car.truck.or van', 'Public transportation (excluding taxicab)', 'Walked',
                           'Taxicab,motorcyle,bicycle or other means']]
    travel_df.columns = ['Car,truck,or van', 'Public transportation', 'Walked',
                         'Taxicab,motorcyle,bicycle or other means']
    travel_df = travel_df.T.reset_index()
    travel_df.columns = ['Vehicle', 'Total']
    return travel_df

def mode_travel(county_name, label_type=0):
    travel_df = pd.read_csv('./Data/Vehicles_county.csv')
    travel_df_state = pd.read_csv('./Data/Vehicles_state.csv')
    travel_df = travel_df[travel_df['NAME'] == county_name]
    travel_df = mode_travel_preproc(travel_df)
    travel_df_state = mode_travel_preproc(travel_df_state)
    if label_type == 1:
        mode = travel_df.iloc[travel_df['Total'].idxmax()]['Vehicle']
        county_per = travel_df[travel_df['Vehicle']==mode]['Total'].tolist()[0]/travel_df['Total'].sum()
        state_per = travel_df_state[travel_df_state['Vehicle'] == mode]['Total'].tolist()[0] / travel_df_state['Total'].sum()
        return mode, round(county_per,2)*100,round(state_per,2)*100
    light_orange = (1.0, 0.6, 0.0)
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.set_style('darkgrid')
    total = sum(travel_df['Total'])
    state_total = sum(travel_df_state['Total'])
    targets = {x: ((y / state_total)) * total for x, y in
               zip(travel_df_state['Vehicle'], travel_df_state['Total'])}
    sns.barplot(x=len(travel_df['Total']) * [total], y=travel_df['Vehicle'], orient='h', color='white',
                width=0.6)
    sns.barplot(x=travel_df['Total'], y=travel_df['Vehicle'], orient='h', color=light_orange, width=0.6)
    # sns.barplot(x=len(race_df['Total'])*[total], y=race_df['Race'], orient='h', color= 'white', width=0.6)
    x, ymins, ymaxs = list(
        zip(*[(targets[v.get_text()], v.get_position()[1] - 0.6 / 2, v.get_position()[1] + 0.6 / 2) for v in
              ax.get_yticklabels()]))
    ax.vlines(x=x, color='black', linestyle='-', linewidth=5, capstyle='butt', ymin=ymins, ymax=ymaxs)
    plot_labels = [f"{x:,}" for x in list(travel_df['Total'])]
    ax.bar_label(ax.containers[0], labels=plot_labels, fontsize=40, label_type='edge', padding=10)
    plt.box(False)
    ax.set_xlabel('', visible=False)
    ax.tick_params(axis='y', which='major', labelsize=54)
    ax.tick_params(axis='x', which='major', labelsize=40)
    xlabels_new = [re.sub("(.{25})", "\\1\n", label, 0, re.DOTALL) for label in travel_df['Vehicle']]
    plt.yticks(range(4), xlabels_new, fontname=font)
    plt.yticks(fontname=font)
    ax.set_ylabel('', visible=False)
    plt.rc('axes', labelsize=5)
    plt.xticks(list(range(0, total+5, total // 5)), [str(x) + '%' for x in list(range(0, 101, 20))])
    plt.savefig(f'./Visualizations/{county_name}_vehicle.png', dpi=300, bbox_inches='tight')


mode_travel('Champaign County',1)

def occupation_preproc(occ_df):
    occ_df.columns = [re.sub('TotalCivilian employed population 16 years and over', '', i) for i in occ_df.columns]
    col_list = ['Management.business.science.and arts occupations', 'Service occupations',
                'Sales and office occupations', 'Natural resources.construction.and maintenance occupations',
                'Production.transportation.and material moving occupations']
    occ_df = occ_df[col_list]
    finalcols = ['Management, science \n& related', 'Services', 'Sales & office', 'Natural Resources \n& maintenance',
                 'Production & Transportation']
    occ_df.columns = finalcols
    occ_df = occ_df.T.reset_index()
    occ_df.columns = ['Occupation', 'Total']
    return occ_df

def occupation(county_name, label_type=0):
    occ_df = pd.read_csv('./Data/Occupation_county.csv')
    occ_df_state = pd.read_csv('./Data/Occupation_state.csv')
    occ_df = occ_df[occ_df['NAME'] == county_name]
    occ_df = occupation_preproc(occ_df)
    occ_df_state = occupation_preproc(occ_df_state)
    if label_type==1:
        occ = occ_df.iloc[occ_df['Total'].idxmax()]['Occupation']
        county_per = occ_df[occ_df['Occupation'] == occ]['Total'].tolist()[0] / occ_df['Total'].sum()
        state_per = occ_df_state[occ_df_state['Occupation'] == occ]['Total'].tolist()[0] / occ_df_state['Total'].sum()
        if round(county_per,2)*100 < round(state_per,2)*100:
            return occ.replace("\n",""), round(county_per,2)*100,round(state_per,2)*100, "lower than"
        elif round(county_per,2)*100 > round(state_per,1)*100:
            return occ.replace("\n",""), round(county_per,2)*100,round(state_per,2)*100, "greater than"
        else:
            return occ.replace("\n",""), round(county_per,2)*100,round(state_per,2)*100, "equal to"
    light_orange = (1.0, 0.6, 0.0)
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.set_style('darkgrid')
    total = sum(occ_df['Total'])
    state_total = sum(occ_df_state['Total'])
    targets = {x: ((y / state_total)) * total for x, y in
               zip(occ_df_state['Occupation'], occ_df_state['Total'])}
    sns.barplot(x=len(occ_df['Total']) * [total], y=occ_df['Occupation'], orient='h', color='white',
                width=0.6)
    sns.barplot(x=occ_df['Total'], y=occ_df['Occupation'], orient='h', color=light_orange, width=0.6)
    # sns.barplot(x=len(race_df['Total'])*[total], y=race_df['Race'], orient='h', color= 'white', width=0.6)
    x, ymins, ymaxs = list(
        zip(*[(targets[v.get_text()], v.get_position()[1] - 0.6 / 2, v.get_position()[1] + 0.6 / 2) for v in
              ax.get_yticklabels()]))
    ax.vlines(x=x, color='black', linestyle='-', linewidth=5, capstyle='butt', ymin=ymins, ymax=ymaxs)
    plot_labels = [f"{x:,}" for x in list(occ_df['Total'])]
    ax.bar_label(ax.containers[0], labels=plot_labels, fontsize=40, label_type='edge', padding=10)
    plt.box(False)
    ax.set_xlabel('', visible=False)
    ax.tick_params(axis='y', which='major', labelsize=50)
    ax.tick_params(axis='x', which='major', labelsize=40)
    plt.yticks(fontname=font)
    ax.set_ylabel('', visible=False)
    plt.rc('axes', labelsize=5)
    plt.xticks(list(range(0, total+5, total // 5)), [str(x) + '%' for x in list(range(0, 101, 20))])
    plt.savefig(f'./Visualizations/{county_name}_occupation.png', dpi=300, bbox_inches='tight')

occupation('Bond County',1)

def industry_preproc(industry_df):
    industry_df.columns = [re.sub('TotalFull-time.year-round civilian employed population 16 years and over', '', col)
                           for col in industry_df.columns]
    cols = ['Agriculture.forestry.fishing and hunting.and mining', 'Construction', 'Manufacturing', 'Wholesale trade',
            'Retail trade', 'Transportation and warehousing.and utilities', 'Information',
            'Finance and insurance.and real estate and rental and leasing',
            'Professional.scientific.and management.and administrative and waste management services',
            'Educational services.and health care and social assistance',
            'Arts.entertainment.and recreation.and accommodation and food services',
            'Other services.except public administration', 'Public administration']
    industry_df = industry_df[cols]
    industry_df.columns = ['Ag, Forestry, Fishing and hunting', 'Construction', 'Manufacturing', 'WholeSale Trade',
                           'Retail Trade', 'Transport, warehouse and utilities', 'Information',
                           'Finance,Insurance and Real estate', 'Prof, mgmt and waste mgmt',
                           'Education,healthcare and social services', 'Arts, entertainment, recreation and food',
                           'Other service', 'Public Admin']
    industry_df = industry_df.T.reset_index()
    industry_df.columns = ['Industry', 'Total']
    return industry_df

def industry(county_name, label_type=0):
    industry_df = pd.read_csv('./Data/Industry_county.csv')
    industry_df_state = pd.read_csv('./Data/Industry_state.csv')
    industry_df = industry_df[industry_df['NAME'] == county_name]
    industry_df = industry_preproc(industry_df)
    industry_df_state = industry_preproc(industry_df_state)
    if label_type==1:
        occ = industry_df.iloc[industry_df['Total'].idxmax()]['Industry']
        county_per = industry_df[industry_df['Industry'] == occ]['Total'].tolist()[0] / industry_df['Total'].sum()
        state_per = industry_df_state[industry_df_state['Industry'] == occ]['Total'].tolist()[0] / industry_df_state['Total'].sum()
        if round(county_per,2) *100 < round(state_per,2) *100:
            return occ.replace("\n",""), round(county_per,2) *100,round(state_per,2) *100, "lesser than"
        elif round(county_per,2) *100 > round(state_per,2) *100:
            return occ.replace("\n",""), round(county_per,2) *100,round(state_per,2) *100, "greater than"
        else:
            return occ.replace("\n",""), round(county_per,2) *100,round(state_per,2) *100, "equal to"
    light_orange = (1.0, 0.6, 0.0)
    fig, ax = plt.subplots(figsize=(16, 35))
    sns.set_style('darkgrid')
    total = sum(industry_df['Total'])
    state_total = sum(industry_df_state['Total'])
    targets = {x: ((y / state_total)) * total for x, y in
               zip(industry_df_state['Industry'], industry_df_state['Total'])}
    sns.barplot(x=len(industry_df['Total']) * [total], y=industry_df['Industry'], orient='h', color='white',
                width=0.6)
    sns.barplot(x=industry_df['Total'], y=industry_df['Industry'], orient='h', color=light_orange, width=0.6)
    # sns.barplot(x=len(race_df['Total'])*[total], y=race_df['Race'], orient='h', color= 'white', width=0.6)
    x, ymins, ymaxs = list(
        zip(*[(targets[v.get_text()], v.get_position()[1] - 0.6 / 2, v.get_position()[1] + 0.6 / 2) for v in
              ax.get_yticklabels()]))
    ax.vlines(x=x, color='black', linestyle='-', linewidth=5, capstyle='butt', ymin=ymins, ymax=ymaxs)
    plot_labels = [f"{x:,}" for x in list(industry_df['Total'])]
    ax.bar_label(ax.containers[0], labels=plot_labels, fontsize=45, label_type='edge', padding=10)
    plt.box(False)
    ax.set_xlabel('', visible=False)
    ax.tick_params(axis='y', which='major', labelsize=60)
    ax.tick_params(axis='x', which='major', labelsize=45)
    xlabels_new = [re.sub("(.{21})", "\\1\n", label, 0, re.DOTALL) for label in industry_df['Industry']]
    plt.yticks(range(13), xlabels_new,fontname=font)
    ax.set_ylabel('', visible=False)
    plt.rc('axes', labelsize=5)
    blue = (0, 0, 0)
    colors = {'State': blue, county_name: light_orange}
    labels = list(colors.keys())
    handles = [plt.Rectangle((0, 0), 0.5, 0.5, color=colors[label]) for label in labels]
    plt.legend(handles, labels, fontsize=55, loc="upper center", bbox_to_anchor=(0.5, -0.038), facecolor="white",
               edgecolor="white")
    plt.xticks(list(range(0, (total+11), total//5)), [str(x) + '%' for x in list(range(0, 101, 20))])
    plt.savefig(f'./Visualizations/{county_name}_industry.png', dpi=300, bbox_inches='tight')

industry('Champaign County')

def vehicle_preproc(vehicle_df):
    vehicle_df = vehicle_df[vehicle_df.columns[2:7]].T.reset_index()
    vehicle_df.columns = ['Vehicle_count', 'Total']
    return vehicle_df

def vehicle_count(county_name, label_type=0):
    vehicle_df = pd.read_csv('./Data/Vehicle_count_county.csv')
    vehicle_df_state = pd.read_csv('./Data/Vehicle_count_state.csv')
    vehicle_df = vehicle_df[vehicle_df['NAME'] == county_name]
    vehicle_df = vehicle_preproc(vehicle_df)
    vehicle_df_state = vehicle_preproc(vehicle_df_state)
    if label_type ==1:
        county_count = vehicle_df.iloc[vehicle_df['Total'].idxmax()]['Vehicle_count']
        state_count = vehicle_df_state.iloc[vehicle_df_state['Total'].idxmax()]['Vehicle_count']
        return county_count, state_count
    light_orange = (1.0, 0.6, 0.0)
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.set_style('darkgrid')
    total = sum(vehicle_df['Total'])
    state_total = sum(vehicle_df_state['Total'])
    targets = {x: ((y / state_total)) * total for x, y in zip(vehicle_df_state['Vehicle_count'], vehicle_df_state['Total'])}
    sns.barplot(x=len(vehicle_df['Total']) * [total], y=vehicle_df['Vehicle_count'], orient='h', color='white', width=0.6)
    sns.barplot(x=vehicle_df['Total'], y=vehicle_df['Vehicle_count'], orient='h', color=light_orange, width=0.6)
    # sns.barplot(x=len(race_df['Total'])*[total], y=race_df['Race'], orient='h', color= 'white', width=0.6)
    x, ymins, ymaxs = list(
        zip(*[(targets[v.get_text()], v.get_position()[1] - 0.6 / 2, v.get_position()[1] + 0.6 / 2) for v in
              ax.get_yticklabels()]))
    ax.vlines(x=x, color='black', linestyle='-', linewidth=5, capstyle='butt', ymin=ymins, ymax=ymaxs)
    plot_labels = [f"{x:,}" for x in list(vehicle_df['Total'])]
    ax.bar_label(ax.containers[0], labels=plot_labels, fontsize=40, label_type='edge', padding=10)
    plt.box(False)
    ax.set_xlabel('', visible=False)
    ax.tick_params(axis='y', which='major', labelsize=55)
    ax.tick_params(axis='x', which='major', labelsize=40)
    plt.yticks(fontname=font)
    ax.set_ylabel('', visible=False)
    plt.rc('axes', labelsize=5)
    plt.xticks(list(range(0, total+20, total//5)), [str(x) + '%' for x in list(range(0, 101, 20))])
    plt.savefig(f'./Visualizations/{county_name}_vehcilecount.png', dpi=300, bbox_inches='tight')

vehicle_count('Champaign County',1)

def language_preproc(lang_df):
    languages_dict = {}
    languages = ['Speak only English', 'Spanish', 'Indo-European languages', 'Asian and Pacific Island languages',
                 'Other languages']
    lang_regex = '|'.join(languages)
    for col in lang_df.columns:
        if re.search('EstimateTotalPopulation', col):
            if re.search(lang_regex, col):
                l = col[re.search(lang_regex, col).start():re.search(lang_regex, col).end()]
                if l not in languages_dict:
                    languages_dict[l] = []
                languages_dict[l].append(col)
    for lang in languages_dict:
        lang_df[lang] = lang_df[languages_dict[lang]].sum(axis=1)
        lang_df.drop(columns=lang_df[languages_dict[lang]], inplace=True, axis=1)
    lang_df.columns = [item.replace("Asian and Pacific Island languages" ,"Asian & Pacific Island languages") for item in lang_df.columns]
    lang_df = lang_df[lang_df.columns[-5:]].T.reset_index()
    lang_df.columns = ['Language', 'Total']
    return lang_df
def language(county_name, label_type=0):
    lang_df = pd.read_csv('./Data/Languages_county.csv')
    lang_df_state = pd.read_csv('./Data/Languages_state.csv')
    lang_df = lang_df[lang_df['NAME'] == county_name]
    lang_df = language_preproc(lang_df)
    lang_df_state = language_preproc(lang_df_state)
    if label_type ==1:
        lang_eng = lang_df[lang_df['Language'] == "Speak only English"]['Total'].tolist()[0]/ lang_df['Total'].sum()
        lang_eng_state = lang_df_state[lang_df_state['Language'] == "Speak only English"]['Total'].tolist()[0]/ \
                         lang_df_state['Total'].sum()
        return round(lang_eng, 2)*100, round(lang_eng_state, 2)*100
    total = sum(lang_df['Total'])
    state_total = sum(lang_df_state['Total'])
    targets = {x:((y/state_total))*total for x,y in zip(lang_df_state['Language'], lang_df_state['Total'])}
    light_orange = (1.0, 0.6, 0.0)
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.set_style('darkgrid')
    sns.barplot(x=len(lang_df['Total']) * [total], y=lang_df['Language'], orient='h', color='white', width=0.6)
    sns.barplot(x=lang_df['Total'], y=lang_df['Language'], orient='h', color=light_orange, width=0.6)
    # sns.barplot(x=len(race_df['Total'])*[total], y=race_df['Race'], orient='h', color= 'white', width=0.6)
    x, ymins, ymaxs = list(
        zip(*[(targets[v.get_text()], v.get_position()[1] - 0.6 / 2, v.get_position()[1] + 0.6 / 2) for v in
              ax.get_yticklabels()]))
    ax.vlines(x=x, color='black', linestyle='-', linewidth=5, capstyle='butt', ymin=ymins, ymax=ymaxs)
    plot_labels = [f"{x:,}" for x in list(lang_df['Total'])]
    ax.bar_label(ax.containers[0], labels=plot_labels, fontsize=40, label_type='edge', padding=10)
    plt.box(False)
    ax.set_xlabel('', visible=False)
    ax.tick_params(axis='y', which='major', labelsize=55)
    ax.tick_params(axis='x', which='major', labelsize=40)
    plt.yticks(fontname=font)
    ax.set_ylabel('', visible=False)
    plt.rc('axes', labelsize=5)
    plt.xticks(list(range(0, total+5, total//5)), [str(x) + '%' for x in list(range(0, 101, 20))])
    plt.savefig(f'./Visualizations/{county_name}_languageimage.png', dpi=300, bbox_inches='tight')

language('Champaign County',1)
def clean_population_cols(df):
    df['0-9 years'] = df['Under 5 years'] + df['5 to 9 years']
    df['10-19 years'] = df['10 to 14 years'] + df['15 to 19 years']
    df['20-29 years'] = df['20 to 24 years'] + df['25 to 29 years']
    df['30-39 years'] = df['30 to 34 years'] + df['35 to 39 years']
    df['40-49 years'] = df['40 to 44 years'] + df['45 to 49 years']
    df['50-59 years'] = df['50 to 54 years'] + df['55 to 59 years']
    df['60-69 years'] = df['60 to 64 years'] + df['65 to 69 years']
    df['70-79 years'] = df['70 to 74 years'] + df['75 to 79 years']
    df['80+ years'] = df['80 to 84 years'] + df['85 years and over']
    df.drop(['Under 5 years', '5 to 9 years', '10 to 14 years',
       '15 to 19 years', '20 to 24 years', '25 to 29 years', '30 to 34 years',
       '35 to 39 years', '40 to 44 years', '45 to 49 years', '50 to 54 years',
       '55 to 59 years', '60 to 64 years', '65 to 69 years', '70 to 74 years',
       '75 to 79 years', '80 to 84 years', '85 years and over'], axis=1, inplace=True)
    return df.T

def pop_p(pop_df):
    pop_df.columns = [col.replace('TotalTotal population', '') for col in pop_df.columns]
    gender_cols = [col for col in pop_df.columns if
                   re.search('Male|Female', col) and not re.search('Percen|SELECTED|SUMMARY', col)]
    pop_df = pop_df[gender_cols]
    dataframe_dict = {'Male': {}, 'Female': {}}
    for col in pop_df.columns:
        if re.search('Male', col):
            temp = re.sub('Male|Total populationAGE', '', col)
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
    x = pd.concat([x, y], axis=1)
    x = clean_population_cols(x.T)
    x.reset_index(inplace=True)
    x.columns = ['Age', 'Male', 'Female']
    x.drop([0], axis=0, inplace=True)
    x['total'] = x['Male'] + x['Female']
    return x
def population_pyramid(county_name, label=0):
    pop_df = pd.read_csv('./Data/Population_by_age_county.csv')
    pop_df_state = pd.read_csv('./Data/Population_by_age_state.csv')
    pop_df = pop_df[pop_df['NAME'] == county_name]
    x = pop_p(pop_df)
    x_state = pop_p(pop_df_state)
    if label == 1:
        max_id = x['total'].idxmax()-1
        age = x.iloc[max_id]['Age']
        percent = x.iloc[max_id]['total']/x['total'].sum()
        return age, round(percent,2)*100
    age_order = list(x['Age'].unique()[::-1])
    fig, ax = plt.subplots(figsize=(27,15))
    male_total = x['Male'].sum()
    female_total = x['Female'].sum()
    x['Male'] = x['Male']*-1
    x_state['Male'] = x_state['Male'] * -1
    male_total_state = x_state['Male'].sum()
    female_total_state = x_state['Female'].sum()
    male_targets = {x: ((y / male_total_state)) * -male_total for x, y in zip(x['Age'], x_state['Male'])}
    female_targets = {x: ((y / female_total_state)) * female_total for x, y in zip(x['Age'], x_state['Female'])}
    blue= (0.0, 0.4, 1.0)
    light_orange = (1.0, 0.6, 0.0)
    ax1 = sns.barplot(x='Male', y='Age', data=x, order=age_order, color=blue, lw =0, width=0.5)
    sns.barplot(x='Female', y='Age', data=x, order=age_order, color=light_orange, lw =0, width=0.5)
    x, ymins, ymaxs = list(
        zip(*[(male_targets[v.get_text()], v.get_position()[1] - 0.6 / 2, v.get_position()[1] + 0.6 / 2) for v in
              ax.get_yticklabels()]))
    ax.vlines(x=x, color='black', linestyle='-', linewidth=4, capstyle='butt', ymin=ymins, ymax=ymaxs)
    x, ymins, ymaxs = list(
        zip(*[(female_targets[v.get_text()], v.get_position()[1] - 0.6 / 2, v.get_position()[1] + 0.6 / 2) for v in
              ax.get_yticklabels()]))
    ax.vlines(x=x, color='black', linestyle='-', linewidth=4, capstyle='butt', ymin=ymins, ymax=ymaxs)
    ax.tick_params(axis='y', which='major', labelsize=48)
    ax.tick_params(axis='x', which='major', labelsize=37)
    plt.yticks(fontname=font)
    tick_list = list(range(-male_total, 1, male_total//4))[:5]
    tick_list.extend(list(range(0,female_total+1, female_total//4))[1:-1])
    labels = [100, 75, 50, 25, 0, 25, 50, 75]
    plt.xticks(tick_list, [str(i) + '%' for i in labels])
    ax.set_xlabel('', visible=False)
    plt.box(False)
    colors = {'Male': blue, 'Female':  light_orange}
    labels = list(colors.keys())
    handles = [plt.Rectangle((0, 0), 0.5, 0.5, color=colors[label]) for label in labels]
    plt.legend(handles, labels, fontsize=35, loc="upper left", facecolor="white", edgecolor="white")
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
    #final_rent_df.reset_index(inplace=True)
    #final_rent_df.columns = ['', county_name, 'State']
    return final_rent_df.T

def income_preproc(income_df):
    income_df = income_df[income_df.columns[4:14]]
    col_list = []
    for c in income_df.columns:
        c = c.replace('|', ',')
        c = c.replace('to', ' - ')
        c = c.replace('HouseholdsTotal', '')
        col_list.append(c)
    income_df.columns = ["Less than $10,000", "$10,000 - 14,999", "$15,000 - 24,999", "$25,000 - 34,999", "$35,000 - 49,999", "$50,000 - 74,999", "$75,000 - 99,999", "$100,000 - 149,999", "$150,000 - 199,999", "$200,000 or more"]
    income_df = income_df.T.reset_index()
    income_df.columns = ['income', 'Percent']
    return income_df
def housing_income(county_name, label_type=0):
    income_df = pd.read_csv('./Data/Household_income_county.csv')
    income_df_state = pd.read_csv('./Data/Household_income_state.csv')
    income_df = income_df[income_df['NAME'] == county_name]
    income_df = income_preproc(income_df)
    income_df_state = income_preproc(income_df_state)
    if label_type == 1:
        max_id = income_df['Percent'].idxmax()
        income_bracket = income_df.iloc[max_id]['income']
        county_percent = income_df.iloc[max_id]['Percent']
        state_percent  = income_df_state[income_df_state['income']== income_bracket]['Percent'].tolist()[0]
        if round(county_percent, 2) > round(state_percent,2):
            return income_bracket, county_percent, "greater"
        elif round(county_percent, 2) < round(state_percent,2):
            return income_bracket, county_percent, "lesser"
        else:
            return income_bracket, county_percent, "equal"
    targets = {x:y for x,y in zip(income_df_state['income'], income_df_state['Percent'])}
    light_orange = (1.0, 0.6, 0.0)
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.set_style('darkgrid')
    sns.barplot(x=len(income_df['Percent']) * [100], y=income_df['income'], orient='h', color='white', width=0.4)
    sns.barplot(x=income_df['Percent'], y=income_df['income'], orient='h', color=light_orange, width=0.6)
    # sns.barplot(x=len(race_df['Total'])*[total], y=race_df['Race'], orient='h', color= 'white', width=0.6)
    x, ymins, ymaxs = list(
        zip(*[(targets[v.get_text()], v.get_position()[1] - 0.6 / 2, v.get_position()[1] + 0.6 / 2) for v in
              ax.get_yticklabels()]))
    ax.vlines(x=x, color='black', linestyle='-', linewidth=4, capstyle='butt', ymin=ymins, ymax=ymaxs)
    plot_labels = [f"{x:,}" for x in list(income_df['Percent'])]
    ax.bar_label(ax.containers[0], labels=plot_labels, fontsize=25, label_type='edge', padding=10)
    plt.box(False)
    ax.set_xlabel('', visible=False)
    ax.tick_params(axis='y', which='major', labelsize=28)
    ax.tick_params(axis='x', which='major', labelsize=25)
    plt.yticks(fontname=font)
    ax.set_ylabel('', visible=False)
    plt.rc('axes', labelsize=5)
    plt.xticks(list(range(0, 101, 20)), [str(x) + '%' for x in list(range(0, 101, 20))])
    plt.savefig(f'./Visualizations/{county_name}_incomeimage.png', dpi=300, bbox_inches='tight')

housing_income('Champaign County',1)

def housing_table(county_name):
    housing_county_df = pd.read_csv('./Data/Housing_Tenure_county.csv')
    housing_state_df = pd.read_csv('./Data/Housing_Tenure_state.csv')
    housing_county_df = housing_county_df[housing_county_df['NAME'] == county_name]
    housing_county_df = housing_county_df[['Abs_Total','Occupied','Vacant']]
    housing_state_df = housing_state_df[['Abs_Total','Occupied','Vacant']]
    housing_county_df = pd.concat([housing_county_df, housing_state_df], axis=0)
    housing_county_df.columns = ['Total Housing Units','Occupied', 'Vacant']
    housing_county_df.reset_index(inplace=True)
    rent_df = housing_rent(county_name)
    rent_df.reset_index(inplace=True)
    housing_county_df = pd.concat([housing_county_df,rent_df], axis=1, join="inner")
    housing_county_df = housing_county_df[['Total Housing Units', 'Occupied', 'Owner occupied',
       'Renter occupied', 'Vacant']]
    housing_county_df = housing_county_df.T
    housing_county_df.reset_index(inplace=True)
    housing_county_df.columns = ['',county_name, 'State']
    housing_county_df.loc[:, ['State']] = housing_county_df['State'].map('{:,.0f}'.format)
    housing_county_df.loc[:, [county_name]] = housing_county_df[county_name].map('{:,.0f}'.format)
    return housing_county_df

housing_table('Champaign County')
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
    state_df.loc[:, ['State']] = state_df['State'].map('{:,.0f}'.format)
    state_df.loc[:, [county_name]] = state_df[county_name].map('{:,.0f}'.format)
    state_df.astype(str)
    state_df.loc[state_df['']== 'Rent > 30% of household income', [county_name,'State']] = state_df.loc[state_df['']== 'Rent > 30% of household income'][[county_name, 'State']] + "%"
    state_df.loc[state_df['']== 'Cost > 30% of household income', [county_name,'State']] = state_df.loc[state_df['']== 'Cost > 30% of household income'][[county_name, 'State']] + "%"
    return state_df

def race_preproc(race_df: pd.DataFrame):
    race_df = race_df[race_df.columns[2:9]]
    final_col_list = []
    for col in race_df.columns:
        if not re.search('Some', col):
            temp = col.replace('alone', '')
            final_col_list.append(temp.strip())
        else:
            final_col_list.append(col)
    final_col_list[final_col_list.index('Native Hawaiian and Other Pacific Islander')] = 'NH and Pacific Islander'
    final_col_list = [item.replace("American Indian and Alaska Native", "American Indian & Alaska Native") for item in final_col_list]
    final_col_list = [col.title() for col in final_col_list]
    final_col_list = [item.replace("Nh And Pacific Islander", "NH and Pacific Islander") for item in final_col_list]
    race_df.columns = final_col_list
    race_df = race_df.T.reset_index()
    race_df.columns = ['Race', 'Total']
    return race_df

def population_by_race(county_name, label_type=0):
    race_df = pd.read_csv('./Data/Population_by_race_county.csv')
    race_df_state = pd.read_csv('./Data/Population_by_race_state.csv')
    race_df = race_df[race_df['NAME'] == county_name]
    race_df = race_preproc(race_df)
    race_df_state = race_preproc(race_df_state)
    state_total = race_df_state['Total'].sum()
    total = race_df['Total'].sum()
    if label_type == 1:
        white_county = race_df[race_df['Race']== 'White']['Total'].tolist()[0]/total
        white_state = race_df_state[race_df_state['Race']== 'White']['Total'].tolist()[0]/race_df_state['Total'].sum()
        if round(white_county,2)*100 > round(white_state,2)*100:
            return round(white_county,2)*100, "less"
        elif round(white_county,2)*100 < round(white_state,2)*100:
            return round(white_county, 2) * 100, "more"
        else:
            return round(white_county, 2) * 100, "equal to"
    targets = {x:((y/state_total))*total for x,y in zip(race_df_state['Race'], race_df_state['Total'])}
    race_df['Percent'] = (race_df['Total']/total)*100
    light_orange = (1.0, 0.6, 0.0)
    fig, ax = plt.subplots(figsize=(9,6))
    sns.set_style('darkgrid')
    sns.barplot(x=len(race_df['Total'])*[total], y=race_df['Race'], orient='h', color= 'white', width=0.6)
    sns.barplot(x=race_df['Total'], y=race_df['Race'], orient='h', color= light_orange, width=0.6)
    #sns.barplot(x=len(race_df['Total'])*[total], y=race_df['Race'], orient='h', color= 'white', width=0.6)
    x, ymins, ymaxs = list(
        zip(*[(targets[v.get_text()], v.get_position()[1] - 0.6 / 2, v.get_position()[1] + 0.6 / 2) for v in
              ax.get_yticklabels()]))
    ax.vlines(x=x, color='black', linestyle='-', linewidth=4, capstyle='butt', ymin=ymins, ymax=ymaxs)
    plot_labels = [f"{x:,}" for x in list(race_df['Total'])]
    ax.bar_label(ax.containers[0], labels=plot_labels, fontsize=20, label_type='edge', padding=10)
    plt.box(False)
    ax.set_xlabel('', visible=False)
    ax.tick_params(axis='y', which='major', labelsize=27)
    ax.tick_params(axis='x', which='major', labelsize=25)
    plt.yticks(fontname=font)
    ax.set_ylabel('', visible=False)
    #plt.rc('axes', labelsize=5)
    plt.xticks(list(range(0,total+1,int(0.2*total))),[str(x)+'%' for x in list(range(0,110,20))])
    plt.savefig(f'./Visualizations/{county_name}_Raceimage.png', dpi=300, bbox_inches='tight')

population_by_race('Champaign County')

def eth_preproc(eth_df):
    eth_df = eth_df[['Not Hispanic or Latino', 'Hispanic or Latino']]
    eth_df = eth_df.T.reset_index()
    eth_df.columns = ['Ethnicity', 'Total']
    return eth_df
def population_by_ethnicity(county_name, label_type=0):
    eth_df = pd.read_csv('./Data/Population_by_ethnicity_county.csv')
    eth_df_state = pd.read_csv('./Data/Population_by_ethnicity_state.csv')
    eth_df = eth_df[eth_df['NAME'] == county_name]
    eth_df = eth_preproc(eth_df)
    eth_df_state = eth_preproc(eth_df_state)
    state_total = eth_df_state['Total'].sum()
    total = eth_df['Total'].sum()
    if label_type == 1:
        hisp_county = eth_df[eth_df['Ethnicity']== 'Hispanic or Latino']['Total'].tolist()[0]/total
        hisp_state = eth_df_state[eth_df_state['Ethnicity']== 'Hispanic or Latino']['Total'].tolist()[0]/eth_df_state['Total'].sum()
        if round(hisp_county,2)*100 > round(hisp_state,2) *100:
            return round(hisp_county,2)*100, "more than", round(hisp_state,2) *100
        elif round(hisp_county,2)*100 < round(hisp_state,2) *100:
            return round(hisp_county, 2) * 100, "less than", round(hisp_state,2) *100
        else:
            return round(hisp_county, 2) * 100, "equal to", round(hisp_state,2) *100
    targets = {x:((y/state_total))*total for x,y in zip(eth_df_state['Ethnicity'], eth_df_state['Total'])}
    eth_df['Percent'] = (eth_df['Total'] / total) * 100
    light_orange = (1.0, 0.6, 0.0)
    black = (0, 0, 0)
    fig, ax = plt.subplots(figsize=(10, 2))
    sns.barplot(x=len(eth_df['Total']) * [total], y=eth_df['Ethnicity'], orient='h', color='white', width=0.3)
    sns.barplot(x=eth_df['Total'], y=eth_df['Ethnicity'], orient='h', color=light_orange, width=0.6)
    x, ymins, ymaxs = list(
        zip(*[(targets[v.get_text()], v.get_position()[1] - 0.6 / 2, v.get_position()[1] + 0.6 / 2) for v in
              ax.get_yticklabels()]))
    ax.vlines(x=x, color='black', linestyle='-', linewidth=4, capstyle='butt', ymin=ymins, ymax=ymaxs)
    plot_labels = [f"{x:,}" for x in list(eth_df['Total'])]
    ax.bar_label(ax.containers[0], labels=plot_labels, fontsize=20, label_type='edge', padding=10)
    plt.box(False)
    plt.tight_layout()
    ax.set_xlabel('', visible=False)
    ax.tick_params(axis='y', which='major', labelsize=27)
    ax.tick_params(axis='x', which='major', labelsize=25)
    plt.yticks(fontname=font)
    ax.set_ylabel('', visible=False)
    plt.rcParams['font.size'] = 12
    colors = {'State': black, county_name: light_orange}
    labels = list(colors.keys())
    handles = [plt.Rectangle((0, 0), 0.5, 0.5, color=colors[label]) for label in labels]
    plt.legend(handles, labels, fontsize=25, loc="upper center", bbox_to_anchor=(0.5, -0.4), facecolor="white", edgecolor="white")
    plt.xticks(list(range(0,total+1,int(0.2*total))), [str(x) + '%' for x in list(range(0, 110, 20))])
    plt.savefig(f'./Visualizations/{county_name}_Ethnicimage.png', dpi=300, bbox_inches='tight')

population_by_ethnicity('Crawford County',1)
