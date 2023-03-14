import pandas as pd
import plotly.figure_factory as ff
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, gray
from Table_Visualizer import housing_table, housing_affordability, housing_rent, commute
import plotly.graph_objects as go
from reportlab.lib.styles import getSampleStyleSheet
import re
styles = getSampleStyleSheet()


def summary(county_name):
    pop_df = pd.read_csv('./Data/Population_by_age_county.csv')
    pop_df_state = pd.read_csv('./Data/Population_by_age_state.csv')
    pop_df = pop_df[pop_df['NAME'] == county_name]
    income_df = pd.read_csv('./Data/Household_income_county.csv')
    income_df_state = pd.read_csv('./Data/Household_income_state.csv')
    median_income = 'HouseholdsMedian income (dollars)'
    income_df = income_df[income_df['NAME'] == county_name]
    median_age = 'TotalTotal populationSUMMARY INDICATORSMedian age (years)'
    total_pop = 'TotalTotal population'
    median_age_value = round(pop_df[median_age].tolist()[0],0)
    median_age_value_state = round(pop_df_state[median_age].tolist()[0],0)
    total_pop_value = pop_df[total_pop].tolist()[0]
    total_pop_value_state = pop_df_state[total_pop].tolist()[0]
    median_income_value = income_df[median_income].tolist()[0]
    median_income_value_state = income_df_state[median_income].tolist()[0]
    poverty_df = pd.read_csv('./Data/Poverty_Status_county.csv')
    print(median_age_value, total_pop_value, median_income_value)
    print(median_age_value_state, total_pop_value_state, median_income_value_state)

summary('Champaign County')



def render_mpl_table(data, name,col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 0.8, 0.8], header_columns=0,
                     ax=None, **kwargs):
    #colorscale = [[0, '#ffffff']]
    header = 'darkslategray' if name != 'commute' else 'white'
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(data.columns),
                    line_color=header,
                    fill_color='white',
                    align='left'),
        cells=dict(values=[data[x] for x in data.columns],
                   fill_color='white',
                   align='left'))
    ])
    fig.update_layout(autosize=True,width=750,height=450,margin = dict(l=0, r=90, t=30, b=50), font_size= 16, font_color = 'black', )
    fig.write_image(f'./Tables/{name}.png')

##Creating Tables
df = housing_table('Champaign County')
render_mpl_table(df, 'Aff', header_columns=0, col_width=2.0)
df1 = housing_affordability('Champaign County')
render_mpl_table(df1, 'Val', header_columns=0, col_width=2.0)
df2 = housing_rent('Champaign County')
render_mpl_table(df2, 'Rent', header_columns=0, col_width=2.0)
df3 = commute('Champaign County')
render_mpl_table(df3, 'commute', header_columns=0, col_width=2.0)

c = canvas.Canvas("sample_report1.pdf", pagesize=letter)

##Pasting visualizations onto report
c.drawImage('./County_images/CHAMPAIGN.png', 385, 615, 220, 145)
c.drawImage('./Visualizations/Champaign County_Ethnicimage.png', 35, 75, 220, 65)
c.drawImage('./Visualizations/Champaign County_Raceimage.png', 20, 170, 250, 150)
c.drawImage('./Visualizations/Champaign County_PopPyramid2.png', 10, 345, 350, 240)
c.drawImage('./Tables/Aff.png', 350, 175, 280, 180)
c.drawImage('./Tables/Rent.png', 350, 110, 280, 180)
c.drawImage('./Tables/Val.png', 350, 45, 280, 180)
c.drawImage('./Visualizations/Champaign County_incomeimage.png', 350, 385, 300, 180)


c.setFont('Helvetica',  10)
d,m = 45,10
c.drawString(50, 633, f"{'Individual Poverty Rate:':<40}  {'19.1%':<39}  {'12.0%':<10}")
c.drawString(50, 648, f"{'Median Household Income:':<35}  {'59,936':<39}  {'57,915':<10}")
c.drawString(50, 663, f"{'Median Age:':<45}  {'33':<42}  {'39':<10}")
c.drawString(50, 678, f"{'Population Density:':<42}  {'201.17':<39}  {'228.28':<10}")
c.drawString(50, 693, f"{'Land Area(mi2):':<43}  {'998':<41}  {'57,915':<10}")
c.drawString(50, 708, f"{'Total Population':<44}  {'205,766':<37}  {'12,873,761':<10}")
c.setFont('Helvetica',  10)
c.setFillColor(gray)
c.drawString(50, 757-d+m, f"{'ACS 2021':<45}  {'Champaign County':<30}  {'State':<10}")
c.setFont('Helvetica',  12)
c.setFillColor(black)
c.drawString(50, 770-d+m, f"{'Quick Facts':<45}")
c.setFont('Helvetica',  16)
c.drawString(50, 784-d+m, f"{'Champaign County':<45}")

c.setFont('Helvetica',  13)
c.drawString(50, 590, f"{'1. Demographics':<45}")
c.setFont('Helvetica',  11)
c.setFillColor(gray)
c.drawString(50, 573, f"{'1.1 Age-Sex Pyramid':<45}")
c.drawString(50, 330, f"{'1.2 Population by Race':<45}")
c.drawString(50, 150, f"{'1.3 Population by Ethnicity':<45}")
c.setFont('Helvetica',  13)
c.setFillColor(black)

c.drawString(350, 590, f"{'2. Income':<45}")
c.drawString(350, 375, f"{'3. Housing':<45}")
c.setFont('Helvetica',  10)
c.setFillColor(gray)
c.drawString(350, 358, f"{'3.1 Housing Occupancy Status':<45}")
c.drawString(350, 290, f"{'3.2 Housing Tenure':<45}")
c.drawString(350, 230, f"{'3.3 Financial Characteristics of Housing units':<45}")
c.drawString(350, 575, f"{'2.1 Household Income':<45}")
c.setFont('Helvetica',  6)
c.drawString(50, 775, f"{'Illinois State Census Data Center'}")
c.drawString(470, 775, f"{'County Profile Reports'}")
c.setFillColor(gray)
c.line(325,610, 325, 75)

c.showPage()

c.drawImage('./Visualizations/Champaign County_vehcilecount.png', 35, 285, 250, 110)
c.drawImage('./Visualizations/Champaign County_languageimage.png', 35, 440, 250, 120)
c.drawImage('./Visualizations/Champaign County_occupation.png', 325, 600, 250, 120)
c.drawImage('./Visualizations/Champaign County_industry.png', 325, 295, 230, 290)
c.drawImage('./Visualizations/Champaign County_education.png', 35, 595, 250, 120)
c.drawImage('./Visualizations/Champaign County_vehicle.png', 35, 145, 250, 120)
c.drawImage('./Tables/commute.png', 35,-55, 300, 180)
c.drawImage('Extension Logo.png', 325, 100, 150, 60)
c.drawImage('logo 2.png', 325, 50, 130, 50)

c.drawString(325, 740, f"{'6. Employment':<45}")
c.drawString(50, 740, f"{'4. Social Charateristics':<45}")
c.drawString(50, 425, f"{'5. Access':<45}")
c.drawString(325, 270, f"{'ABOUT':<45}")

c.setFont('Helvetica',  10)
c.setFillColor(gray)
c.drawString(50, 725, f"{'4.1 Educational Attainment':<45}")
c.drawString(50, 570, f"{'4.2 Languages spoken at home':<45}")
c.drawString(50, 405, f"{'5.1 Number of vehicles in a household':<45}")
c.drawString(50, 270, f"{'5.2 Mode of travel to work':<45}")
c.drawString(50, 120, f"{'5.3 Inflow/Outflow Job Counts':<45}")
c.drawString(325, 725, f"{'6.1 Number of people employed by occupation':<45}")
c.drawString(325, 590, f"{'6.2 Number of people employed by industry':<45}")
c.drawString(325, 260, f"Data prepared by the Illinois State Census Data Center" )
c.drawString(325, 250, f"Data Sources – ACS 2021 5 Year Tables – [1 to 5.2]")
c.drawString(325, 240, f"                           LEHD, US Census, 2019 – [5.3]")
c.drawString(325, 230, f"                           Bureau of Labor Statistics – [6]")
c.setFont('Helvetica',  10)
c.drawString(335, 215, f"University of Illinois, US Department of Agriculture,")
c.drawString(335, 205, f"Local Extension Councils Cooperating. University of")
c.drawString(335, 195, f"Illinois provides equal opportunities in programs and")
c.drawString(335, 185, f"employment. If you experience any problems accessing")
c.drawString(335, 175, f"or receiving this content, or have feedback on the")
c.drawString(335, 165, f"design, please email, extension@illinois.edu.")

c.setFont('Helvetica',  6)
c.drawString(50, 775, f"{'Illinois State Census Data Center'}")
c.drawString(470, 775, f"{'County Profile Reports'}")
c.setFillColor(gray)
c.line(310, 750, 310, 70)
c.line(310, 285, 580, 285)

c.save()

# Draw fourth image
