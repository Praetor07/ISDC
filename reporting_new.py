import plotly.figure_factory as ff
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
from reportlab.lib.colors import black, gray
from Table_Visualizer import housing_table, housing_affordability, housing_rent
import plotly.graph_objects as go


def render_mpl_table(data, name,col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 0.8, 0.8], header_columns=0,
                     ax=None, **kwargs):
    #colorscale = [[0, '#ffffff']]
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(data.columns),
                    line_color='darkslategray',
                    fill_color='white',
                    align='left'),
        cells=dict(values=[data[x] for x in data.columns],
                   fill_color='white',
                   align='left'))
    ])
    fig.update_layout(autosize=True,width=750,height=450,margin = dict(l=0, r=90, t=30, b=50), font_size= 16, font_color = 'black', )
    fig.write_image(f'{name}.png')


df = housing_table('Champaign County')
render_mpl_table(df, 'Aff', header_columns=0, col_width=2.0)

df1 = housing_affordability('Champaign County')
render_mpl_table(df1, 'Val', header_columns=0, col_width=2.0)

df2 = housing_rent('Champaign County')
render_mpl_table(df2, 'Rent', header_columns=0, col_width=2.0)

image = 'PopPyramid2.png'

# Create a PDF canvas
c = canvas.Canvas("sample_report.pdf", pagesize=letter)

# Draw first image
c.drawImage('CHAMPAIGN.png', 385, 650, 220, 115)
c.drawImage('Ethnicimage.png', 35, 155, 220, 65)
c.drawImage('Raceimage.png', 20, 260, 260, 150)
c.drawImage('PopPyramid2.png', 50, 415, 280, 230)
c.drawImage('Aff.png', 350, 235, 280, 180)
c.drawImage('Rent.png', 350, 170, 280, 180)
c.drawImage('Val.png', 350, 105, 280, 180)
c.drawImage('incomeimage.png', 350, 445, 300, 180)


c.setFont('Helvetica',  8)
d,m = 40,10
c.drawString(50, 703-d+m, f"{'Individual Poverty Rate:':<40}  {'19.1%':<39}  {'12.0%':<10}")
c.drawString(50, 712-d+m, f"{'Median Household Income:':<35}  {'59,936':<39}  {'57,915':<10}")
c.drawString(50, 721-d+m, f"{'Median Age:':<45}  {'33':<42}  {'39':<10}")
c.drawString(50, 730-d+m, f"{'Population Density:':<42}  {'201.17':<39}  {'228.28':<10}")
c.drawString(50, 739-d+m, f"{'Land Area(mi2):':<43}  {'998':<41}  {'57,915':<10}")
c.drawString(50, 748-d+m, f"{'Total Population':<44}  {'205,766':<37}  {'12,873,761':<10}")
c.setFont('Helvetica',  8)
c.setFillColor(gray)
c.drawString(50, 757-d+m, f"{'ACS 2021':<45}  {'Champaign County':<29}  {'State':<10}")
c.setFont('Helvetica',  12)
c.setFillColor(black)
c.drawString(50, 770-d+m, f"{'Quick Facts':<45}")
c.setFont('Helvetica',  16)
c.drawString(50, 784-d+m, f"{'Champaign County':<45}")

c.setFont('Helvetica',  13)
c.drawString(50, 640, f"{'1. Demographics':<45}")
c.setFont('Helvetica',  10)
c.setFillColor(gray)
c.drawString(50, 623, f"{'1.1 Age-Sex Pyramid':<45}")
c.drawString(50, 420, f"{'1.2 Population by Race':<45}")
c.drawString(50, 225, f"{'1.3 Population by Ethnicity':<45}")
c.setFont('Helvetica',  13)
c.setFillColor(black)

c.drawString(350, 640, f"{'2. Income':<45}")
c.drawString(350, 435, f"{'3. Housing':<45}")
c.setFont('Helvetica',  10)
c.setFillColor(gray)
c.drawString(350, 418, f"{'3.1 Housing Occupancy Status':<45}")
c.drawString(350, 350, f"{'3.2 Housing Tenure':<45}")
c.drawString(350, 290, f"{'3.3 Financial Characteristics of Housing units':<45}")
c.drawString(350, 625, f"{'2.1 Household Income':<45}")
c.setFont('Helvetica',  6)
c.drawString(50, 775, f"{'Illinois State Census Data Center'}")
c.drawString(470, 775, f"{'County Profile Reports'}")
c.setFillColor(gray)
#c.line(50,650, 600, 650)
c.line(325,650, 325, 110)

c.save()

# Draw fourth image
