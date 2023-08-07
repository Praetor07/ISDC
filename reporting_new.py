import pandas as pd
import math
import plotly.figure_factory as ff
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, gray
from Table_Visualizer import housing_table, housing_affordability, housing_rent, commute, education_att, mode_travel, occupation, industry, vehicle_count, language, population_pyramid, housing_income, population_by_race, population_by_ethnicity
import plotly.graph_objects as go
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, cm
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
import re
styles = getSampleStyleSheet()


def add_label(county_name, image_type:str):
    if image_type == "population":
        age, percent = population_pyramid(county_name, 1)
        return f"The largest age cohort in the county is {age} representing {percent:.1f} percent\n of the population."
    elif image_type == "race":
        percent, relation = population_by_race(county_name, 1)
        return f"{percent:.1f} percent of the county population identify as white. The county is {relation}\n racially diverse than the state."
    elif image_type == "ethnic":
        per_county, relation, per_state = population_by_ethnicity(county_name, 1)
        return f"{per_county:.1f} percent of the county population identify as Hispanic or Latino. This percentage\n is {relation} the state average of {per_state:.1f} percent."
    elif image_type == "income":
        bracket, county_per, relation = housing_income(county_name, 1)
        return f"The largest household income bracket in the county is {bracket},\n representing {county_per:.1f} percent of households. There are a {relation} percentage of\n households in this bracket in the county when compared to the state."
    elif image_type == "education":
        county_edu, state_edu = education_att(county_name,1)
        return f"The percentage of the county’s residents 25 years and older that have a\n Bachelor’s degree or higher is {county_edu:.1f}, compared to {state_edu:.1f} for the state."
    elif image_type == "language":
        county_lang, state_lang = language(county_name, 1)
        return f"{county_lang} percent of county residents speak only English at home compared\n to {state_lang:.1f} percent for the state."
    elif image_type == "vehiclecount":
        county_count, state_count = vehicle_count(county_name,1)
        conj = "also" if county_count == state_count else ''
        return f"The largest proportion of households in the county have {county_count}.\n In comparison, the largest proportion of households in the state {conj} have\n {state_count}."
    elif image_type == "vehicle":
        mode, county_per, state_per = mode_travel(county_name, 1)
        return f"The most popular mode of transportation in the county is {mode}. {county_per:.1f}\n percent of county households use this to commute to work. In comparison,\n{state_per:.1f} percent of the state’s households use this mode of transportation."
    elif image_type == "occupation":
        occ, county_percent, state_percent, relation = occupation(county_name, 1)
        return f"The top occupation in the county in terms of employment is\n {occ}, employing {county_percent:.1f} percent of all employees.\n This is {relation} the proportion of employees working in the occupation\n at the state level, which is {state_percent:.1f} percent."
    elif image_type == "industry":
        occ, county_percent, state_percent, relation = industry(county_name, 1)
        return f"The top industry in the county in terms of employment is\n {occ}, employing {county_percent:.1f} percent of\n all employees.This is {relation} the proportion of employees working\n in the industry at the state level, which is {state_percent:.1f} percent."


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
    density_df = pd.read_csv('./Data/county_density.csv')
    density = density_df.loc[density_df['NAME.x'] == f"{county_name}, Illinois", ['Land_area','pop_density']].values.tolist()[0]
    county_land_area, county_pop_density = density[0], density[1]
    state_density_df = pd.read_csv('./Data/state_density.csv')
    s_density = state_density_df.loc[state_density_df['NAME.x'] == f"Illinois", ['Land_area', 'pop_density']].values.tolist()[0]
    state_land_area, state_pop_density = s_density[0], s_density[1]
    county_summary_d = {'median_age' :  math.trunc(median_age_value), 'total_pop' : total_pop_value, 'median_income' : median_income_value, 'poverty' : poverty_perc, 'land_area' : math.trunc(round(county_land_area,0)), 'pop_density': round(county_pop_density, 1)}
    state_summary_d = {'median_age' :  math.trunc(median_age_value_state), 'total_pop' : total_pop_value_state, 'median_income' : median_income_value_state, 'poverty' : poverty_perc_state, 'land_area' : math.trunc(round(state_land_area,0)), 'pop_density': round(state_pop_density, 1)}
    county_summary = {x:'{:,}'.format(y) for x,y in county_summary_d.items()}
    state_summary = {x: '{:,}'.format(y) for x,y in state_summary_d.items()}
    return county_summary, state_summary

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
    #print(table)
    # exit()
    df_table = [list(df.iloc[[i]]) for i in range(0, len(df))]
    table_formatted = Table(table)
    table_formatted.setStyle(style)
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

    c = canvas.Canvas(f"./Reports/{county_name}_report.pdf", pagesize=letter)
    county, state = summary(county_name)
    ##Pasting visualizations onto report
    county_name_list = county_name.split(" ")
    county_image = county_name_list[0].upper() if len(county_name_list)==2 else "".join(county_name_list[:-1]).upper()
    c.drawImage(f'./County_images/{county_image}.png', 385, 615, 220, 160)
    c.drawImage(f'./Visualizations/{county_name}_Ethnicimage.png', 55, 40, 260, 90)
    c.setFont('Times-Italic',  8)
    c.setFillColor(gray)
    textobject = c.beginText(55, 35)
    eth_text = add_label(county_name, "ethnic")
    for line in eth_text.splitlines(False):
        textobject.textLine(line.rstrip())
    c.drawText(textobject)
    c.drawImage(f'./Visualizations/{county_name}_Raceimage.png', 10, 180, 320, 140)
    textobject = c.beginText(55, 170)
    race_text = add_label(county_name, "race")
    for line in race_text.splitlines(False):
        textobject.textLine(line.rstrip())
    c.drawText(textobject)
    c.drawImage(f'./Visualizations/{county_name}_PopPyramid2.png', 6, 355, 350, 240)
    textobject = c.beginText(55, 355)
    pop_text = add_label(county_name, "population")
    for line in pop_text.splitlines(False):
        textobject.textLine(line.rstrip())
    c.drawText(textobject)
    #c.drawImage('./Tables/Aff.png', 350, 175, 280, 180)
    #c.drawImage('./Tables/Rent.png', 350, 110, 280, 180)
    #c.drawImage('./Tables/Val.png', 350, 45, 280, 180)
    c.drawImage(f'./Visualizations/{county_name}_incomeimage.png', 350, 397, 250, 190)
    textobject = c.beginText(350, 390)
    income_text = add_label(county_name, "income")
    for line in income_text.splitlines(False):
        textobject.textLine(line.rstrip())
    c.drawText(textobject)

    tb(c, 4.67, 0.1, df1)
    #tb(c, 5, 3.0, df2)
    tb(c, 5.35, 2.65, df, "LEFT")
    poverty_county, age_county, pop_county, income_county, land_area_county, pop_density_county = county['poverty'], county['median_age'], county['total_pop'], county['median_income'], county['land_area'], county['pop_density']
    poverty_state, age_state, pop_state, income_state, land_area_state, pop_density_state = state['poverty'], state['median_age'], state['total_pop'], state['median_income'], state['land_area'], state['pop_density']
    c.setFont('Times-Roman',  10)
    c.setFillColor(black)
    d,m = 45,10
    c.drawString(50, 633, f"{'Individual Poverty Rate:':<39}  {f'{poverty_county}%':<40}  {f'{poverty_state}%':<10}")
    c.drawString(50, 648, f"{'Median Household Income:':<34}  {f'{income_county}':<40}  {f'{income_state}':<10}")
    c.drawString(50, 663, f"{'Median Age:':<45}  {f'{age_county}':<42}  {f'{age_state}':<10}")
    c.drawString(50, 678, f"{'Population Density:':<42}  {f'{pop_density_county}':<41}  {f'{pop_density_state}':<10}")
    c.drawString(50, 693, f"{'Land Area(mi2):':<43}  {f'{land_area_county}':<42}  {f'{land_area_state}':<10}")
    c.drawString(50, 708, f"{'Total Population':<44}  {f'{pop_county}':<40}  {f'{pop_state}':<10}")
    c.setFont('Times-Roman',  10)
    c.setFillColor(gray)
    c.drawString(50, 757-d+m, f"{'ACS 2021':<45}  {f'{county_name}':<30}  {'State':<10}")
    c.setFont('Times-Roman',  12)
    c.setFillColor(black)
    c.drawString(50, 770-d+m, f"{'Quick Facts':<45}")
    c.setFont('Times-Roman',  16)
    c.drawString(50, 784-d+m, f"{county_name:<45}")

    c.setFont('Times-Roman',  13)
    c.drawString(50, 600, f"{'1. Demographics':<45}")
    c.setFont('Times-Roman',  11)
    c.setFillColor(black)
    c.drawString(50, 583, f"{'1.1 Population Pyramid':<45}")
    c.drawString(50, 320, f"{'1.2 Population by Race':<45}")
    c.drawString(50, 135, f"{'1.3 Population by Ethnicity':<45}")
    c.setFont('Times-Roman',  13)
    c.setFillColor(black)

    c.drawString(350, 600, f"{'2. Income':<45}")
    c.drawString(350, 355, f"{'3. Housing':<45}")
    c.setFont('Times-Roman',  11)
    c.setFillColor(black)
    c.drawString(350, 338, f"{'3.1 Housing Occupancy Status':<45}")
    #c.drawString(350, 250, f"{'3.2 Housing Tenure':<45}")
    c.drawString(350, 180, f"{'3.2 Financial Characteristics of Housing units':<45}")
    c.drawString(350, 585, f"{'2.1 Household Income':<45}")
    c.setFont('Times-Roman',  6)
    c.setFillColor(gray)
    c.drawString(50, 775, f"{'Illinois State Census Data Center'}")
    c.drawString(470, 775, f"{'County Profile Reports'}")
    c.setFillColor(gray)
    c.line(330,610, 330, 15)

    c.showPage()
    from reportlab.lib.utils import ImageReader
    c.setFillColor(black)
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
    #print("UOUOU", draw_width, draw_height)
    c.setFont('Times-Italic',  8)
    c.setFillColor(gray)
    c.drawImage(f'./Visualizations/{county_name}_vehcilecount.png', 30, 300, 260, 110)
    textobject = c.beginText(45, 290)
    vehiclecount_text = add_label(county_name, "vehiclecount")
    for line in vehiclecount_text.splitlines(False):
        textobject.textLine(line.rstrip())
    c.drawText(textobject)
    c.drawImage(f'./Visualizations/{county_name}_languageimage.png', 10, 465, 285, 110)
    textobject = c.beginText(45, 455)
    lang_text = add_label(county_name, "language")
    for line in lang_text.splitlines(False):
        textobject.textLine(line.rstrip())
    c.drawText(textobject)
    c.drawImage(f'./Visualizations/{county_name}_occupation.png', 310, 610, 290, 120)
    textobject = c.beginText(350, 600)
    occ_text = add_label(county_name, "occupation")
    for line in occ_text.splitlines(False):
        textobject.textLine(line.rstrip())
    c.drawText(textobject)
    c.drawImage(f'./Visualizations/{county_name}_industry.png', 325, 217, 250, 345)
    textobject = c.beginText(350, 212)
    industry_text = add_label(county_name, "industry")
    for line in industry_text.splitlines(False):
        textobject.textLine(line.rstrip())
    c.drawText(textobject)
    c.drawImage(f'./Visualizations/{county_name}_education.png', 15, 615, 290,120)
    textobject = c.beginText(45, 605)
    edu_text = add_label(county_name, "education")
    for line in edu_text.splitlines(False):
        textobject.textLine(line.rstrip())
    c.drawText(textobject)
    c.drawImage(f'./Visualizations/{county_name}_vehicle.png', 35, 145, 260, 110)
    textobject = c.beginText(45, 135)
    vehicle_text = add_label(county_name, "vehicle")
    for line in vehicle_text.splitlines(False):
        textobject.textLine(line.rstrip())
    c.drawText(textobject)
    #c.drawImage('./Tables/commute.png', 35,-55, 300, 180)
    tb(c, 0.24, 0.45, df3, "CENTER", colors.black)
    #c.drawImage('Extension Logo.png', 325, 40, 160, 55)
    #c.drawImage('logo 2.png', 325, 50, 130, 50)
    c.setFont('Times-Roman', 13)
    c.setFillColor(black)
    c.drawString(325, 750, f"{'6. Employment':<45}")
    c.drawString(50, 750, f"{'4. Social Charateristics':<45}")
    c.drawString(50, 430, f"{'5. Access':<45}")
    c.drawString(325, 155, f"{'ABOUT':<45}")
    c.setFont('Times-Roman',  10)
    c.setFillColor(black)
    c.drawString(50, 735, f"{'4.1 Educational Attainment':<45}")
    c.drawString(50, 580, f"{'4.2 Languages spoken at home':<45}")
    c.drawString(50, 415, f"{'5.1 Number of vehicles in a household':<45}")
    c.drawString(50, 255, f"{'5.2 Mode of travel to work':<45}")
    c.drawString(50, 100, f"{'5.3 Inflow/Outflow Job Counts':<45}")
    c.drawString(325, 735, f"{'6.1 Number of people employed by occupation':<45}")
    c.drawString(325, 555, f"{'6.2 Number of people employed by industry':<45}")
    c.drawString(325, 140, f"Data prepared by the Illinois State Census Data Center")
    c.drawString(325, 127, f"Data Sources – ACS 2021 5 Year Tables – [1 to 5.2]")
    c.drawString(325, 114, f"                           LEHD, US Census, 2019 – [5.3]")
    c.drawString(325, 101, f"                           Bureau of Labor Statistics – [6]")
    c.setFont('Times-Roman',  10)
    c.drawString(325, 88, f"University of Illinois, US Department of Agriculture,")
    c.drawString(325, 75, f"Local Extension Councils Cooperating. University of")
    c.drawString(325, 62, f"Illinois provides equal opportunities in programs and")
    c.drawString(325, 49, f"employment. If you experience any problems accessing")
    c.drawString(325, 36, f"or receiving this content, or have feedback on the")
    c.drawString(325, 23, f"design, please email, extension@illinois.edu.")
    c.setFont('Times-Roman',  6)
    c.setFillColor(gray)
    c.drawString(50, 775, f"{'Illinois State Census Data Center'}")
    c.drawString(470, 775, f"{'County Profile Reports'}")
    c.setFillColor(gray)
    c.line(310, 750, 310, 30)
    c.line(310, 175, 580, 175)
    c.save()

from PyPDF2 import PdfReader, PdfMerger, PdfWriter
def append(count_name):
    first_pdf_path = f"./Reports/{count_name}_report.pdf"
    first_pdf = PdfReader(first_pdf_path)

    # Open the second PDF document to be appended
    second_pdf_path = "Data_Profile Glossary.pdf"
    second_pdf = PdfReader(second_pdf_path)

    # Create a PDF merger object
    output_pdf = PdfWriter()

    # Append the pages from the first PDF
    for page_num in range(len(first_pdf.pages)):
        output_pdf.add_page(first_pdf.pages[page_num])

    # Append the first page from the second PDF
    output_pdf.add_page(second_pdf.pages[0])

    # Save the merged PDF to a new file
    output_pdf_path = f"./Reports/{count_name}_report.pdf"
    with open(output_pdf_path, "wb") as output_file:
        output_pdf.write(output_file)

    # Close the PDF files


if __name__ == '__main__':
    file = pd.read_csv('./Data/Household_income_county.csv')
    for county in file['NAME']:
        print(county, " is running...")
        create_report(county)
        append(county)
        #exit()