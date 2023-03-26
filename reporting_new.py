import pandas as pd
import plotly.figure_factory as ff
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, gray
from Table_Visualizer import housing_table, housing_affordability, housing_rent, commute, education_att, mode_travel, occupation, industry, vehicle_count, language, population_pyramid, housing_income, population_by_race, population_by_ethnicity
import plotly.graph_objects as go
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
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
    poverty_df_state = pd.read_csv('./Data/Poverty_Status_state.csv')
    poverty_df = poverty_df[poverty_df['NAME'] == county_name]
    pov_col = 'Percent below poverty levelPopulation for whom poverty status is determined'
    poverty_perc, poverty_perc_state = poverty_df[pov_col].values.tolist()[0], poverty_df_state[pov_col].values.tolist()[0]
    print(median_age_value, total_pop_value, median_income_value, poverty_perc)
    print(median_age_value_state, total_pop_value_state, median_income_value_state, poverty_perc_state)

summary('Champaign County')
exit()
def tb(c, a, y, df, flag="CENTER", col = colors.grey):
    # Set table style
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 2), (0, 2), flag),
        ('ALIGN', (0, -1), (0, -1), flag),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, 0), 8.5),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (-1, 0), (-1, -1), col),
        #('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 1), (-1, -1), 8.5),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, -2), 1, colors.grey),
        ('LINEAFTER', (0, 0), (-2, -1), 1, colors.grey),
    ]

    # Create a table object
    df = df.astype(str)
    # table = [data[0]] + [map(str, row) for row in data[1:]]
    col = df.columns.tolist()
    x = df[df.columns].values.tolist()
    x_ = [map(str, p) for p in x]
    table = [col] + x_
    print(table)
    # exit()
    df_table = [list(df.iloc[[i]]) for i in range(0, len(df))]
    table_formatted = Table(table)
    table_formatted.setStyle(style)
# Draw the table on the canvas
    table_formatted.wrapOn(c, inch * 1, inch * 1)
    table_formatted.drawOn(c, inch * a, inch * y)
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
def create_report(county_name):
    education_att(county_name)
    commute(county_name)
    mode_travel(county_name)
    occupation(county_name)
    industry(county_name)
    vehicle_count(county_name)
    language(county_name)
    population_pyramid(county_name)
    housing_income(county_name)
    population_by_race(county_name)
    population_by_ethnicity(county_name)
    df = housing_table(county_name)
    render_mpl_table(df, 'Aff', header_columns=0, col_width=2.0)

    df1 = housing_affordability(county_name)
    render_mpl_table(df1, 'Val', header_columns=0, col_width=2.0)
    df2 = housing_rent(county_name)
    render_mpl_table(df2, 'Rent', header_columns=0, col_width=2.0)
    df3 = commute(county_name)
    render_mpl_table(df3, 'commute', header_columns=0, col_width=2.0)

    c = canvas.Canvas(f"{county_name}_sample_report1.pdf", pagesize=letter)

    ##Pasting visualizations onto report
    c.drawImage('./County_images/CHAMPAIGN.png', 385, 615, 220, 160)
    c.drawImage(f'./Visualizations/{county_name}_Ethnicimage.png', 50, 55, 260, 90)
    c.drawImage(f'./Visualizations/{county_name}_Raceimage.png', 5, 180, 320, 140)
    c.drawImage(f'./Visualizations/{county_name}_PopPyramid2.png', 6, 345, 370, 240)
    #c.drawImage('./Tables/Aff.png', 350, 175, 280, 180)
    #c.drawImage('./Tables/Rent.png', 350, 110, 280, 180)
    #c.drawImage('./Tables/Val.png', 350, 45, 280, 180)
    c.drawImage(f'./Visualizations/{county_name}_incomeimage.png', 350, 385, 250, 190)
    tb(c, 4.67, 0.4, df1)
    #tb(c, 5, 3.0, df2)
    tb(c, 5.35, 2.95, df, "LEFT")

    c.setFont('Times-Roman',  10)
    d,m = 45,10
    c.drawString(50, 633, f"{'Individual Poverty Rate:':<40}  {'19.1%':<39}  {'12.0%':<10}")
    c.drawString(50, 648, f"{'Median Household Income:':<35}  {'59,936':<39}  {'57,915':<10}")
    c.drawString(50, 663, f"{'Median Age:':<45}  {'33':<42}  {'39':<10}")
    c.drawString(50, 678, f"{'Population Density:':<42}  {'201.17':<39}  {'228.28':<10}")
    c.drawString(50, 693, f"{'Land Area(mi2):':<43}  {'998':<41}  {'57,915':<10}")
    c.drawString(50, 708, f"{'Total Population':<44}  {'205,766':<37}  {'12,873,761':<10}")
    c.setFont('Times-Roman',  10)
    c.setFillColor(gray)
    c.drawString(50, 757-d+m, f"{'ACS 2021':<45}  {'Champaign County':<30}  {'State':<10}")
    c.setFont('Times-Roman',  12)
    c.setFillColor(black)
    c.drawString(50, 770-d+m, f"{'Quick Facts':<45}")
    c.setFont('Times-Roman',  16)
    c.drawString(50, 784-d+m, f"{county_name:<45}")

    c.setFont('Times-Roman',  13)
    c.drawString(50, 590, f"{'1. Demographics':<45}")
    c.setFont('Times-Roman',  11)
    c.setFillColor(gray)
    c.drawString(50, 573, f"{'1.1 Age-Sex Pyramid':<45}")
    c.drawString(50, 330, f"{'1.2 Population by Race':<45}")
    c.drawString(50, 150, f"{'1.3 Population by Ethnicity':<45}")
    c.setFont('Times-Roman',  13)
    c.setFillColor(black)

    c.drawString(350, 590, f"{'2. Income':<45}")
    c.drawString(350, 375, f"{'3. Housing':<45}")
    c.setFont('Times-Roman',  11)
    c.setFillColor(gray)
    c.drawString(350, 358, f"{'3.1 Housing Occupancy Status':<45}")
    #c.drawString(350, 250, f"{'3.2 Housing Tenure':<45}")
    c.drawString(350, 200, f"{'3.3 Financial Characteristics of Housing units':<45}")
    c.drawString(350, 575, f"{'2.1 Household Income':<45}")
    c.setFont('Times-Roman',  6)
    c.drawString(50, 775, f"{'Illinois State Census Data Center'}")
    c.drawString(470, 775, f"{'County Profile Reports'}")
    c.setFillColor(gray)
    c.line(330,610, 330, 35)

    c.showPage()
    from reportlab.lib.utils import ImageReader
    image = ImageReader(f'./Visualizations/{county_name}_education.png')
    image_width, image_height = image.getSize()
    image_aspect_ratio = image_width / image_height

    # Get the dimensions of the canvas
    canvas_width, canvas_height = c._pagesize
    canvas_aspect_ratio = canvas_width / canvas_height

#    print(canvas_aspect_ratio,canvas_width,canvas_height, "Image", image_aspect_ratio, image_width, image_height)

    # Calculate the dimensions to draw the image at
    if image_aspect_ratio > canvas_aspect_ratio:
        draw_width = canvas_width
        draw_height = canvas_width / image_aspect_ratio
    else:
        draw_width = canvas_height * image_aspect_ratio
        draw_height = canvas_height
    print("UOUOU", draw_width, draw_height)
    c.drawImage(f'./Visualizations/{county_name}_vehcilecount.png', 25, 285, 260, 110)
    c.drawImage(f'./Visualizations/{county_name}_languageimage.png', 0, 450, 295, 110)
    c.drawImage(f'./Visualizations/{county_name}_occupation.png', 310, 600, 300, 120)
    c.drawImage(f'./Visualizations/{county_name}_industry.png', 325, 255, 250, 335)
    c.drawImage(f'./Visualizations/{county_name}_education.png', 12, 595, 295,120)
    c.drawImage(f'./Visualizations/{county_name}_vehicle.png', 25, 150, 260, 110)
    #c.drawImage('./Tables/commute.png', 35,-55, 300, 180)
    tb(c, 0.24, 0.72, df3, "CENTER", colors.black)
    c.drawImage('Extension Logo.png', 325, 40, 160, 55)
    #c.drawImage('logo 2.png', 325, 50, 130, 50)

    c.setFont('Times-Roman', 13)
    c.setFillColor(black)
    c.drawString(325, 740, f"{'6. Employment':<45}")
    c.drawString(50, 740, f"{'4. Social Charateristics':<45}")
    c.drawString(50, 425, f"{'5. Access':<45}")
    c.drawString(325, 235, f"{'ABOUT':<45}")

    c.setFont('Times-Roman',  10)
    c.setFillColor(gray)
    c.drawString(50, 725, f"{'4.1 Educational Attainment':<45}")
    c.drawString(50, 570, f"{'4.2 Languages spoken at home':<45}")
    c.drawString(50, 405, f"{'5.1 Number of vehicles in a household':<45}")
    c.drawString(50, 270, f"{'5.2 Mode of travel to work':<45}")
    c.drawString(50, 120, f"{'5.3 Inflow/Outflow Job Counts':<45}")
    c.drawString(325, 725, f"{'6.1 Number of people employed by occupation':<45}")
    c.drawString(325, 590, f"{'6.2 Number of people employed by industry':<45}")
    c.drawString(325, 220, f"Data prepared by the Illinois State Census Data Center" )
    c.drawString(325, 207, f"Data Sources – ACS 2021 5 Year Tables – [1 to 5.2]")
    c.drawString(325, 194, f"                           LEHD, US Census, 2019 – [5.3]")
    c.drawString(325, 181, f"                           Bureau of Labor Statistics – [6]")
    c.setFont('Times-Roman',  10)
    c.drawString(325, 168, f"University of Illinois, US Department of Agriculture,")
    c.drawString(325, 155, f"Local Extension Councils Cooperating. University of")
    c.drawString(325, 142, f"Illinois provides equal opportunities in programs and")
    c.drawString(325, 129, f"employment. If you experience any problems accessing")
    c.drawString(325, 116, f"or receiving this content, or have feedback on the")
    c.drawString(325, 103, f"design, please email, extension@illinois.edu.")

    c.setFont('Times-Roman',  6)
    c.drawString(50, 775, f"{'Illinois State Census Data Center'}")
    c.drawString(470, 775, f"{'County Profile Reports'}")
    c.setFillColor(gray)
    c.line(310, 750, 310, 30)
    c.line(310, 250, 580, 250)

    c.save()

if __name__ == '__main__':
    create_report('Champaign County')