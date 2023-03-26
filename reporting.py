from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import seaborn as sns
import matplotlib.pyplot as plt
from reportlab.platypus import Table, TableStyle
from Table_Visualizer import housing_table, housing_affordability

font = "Times New Roman"
data = {'x': ['Categorical variable 1', 'Dummy text 3', 'Filers part 4', 'Ghost dataa 2'],
        'y': [10000, 5, 8, 12],
        'a' : [-5,-8,-9,-10]}

total = max(data['y'])
c = canvas.Canvas("dummy.pdf", pagesize=letter)
canvas_width, canvas_height = c._pagesize
print(canvas_width, canvas_height)
fig, ax = plt.subplots(figsize=(20,15))
blue= (0.67,  0.75, 0.90)
light_orange = (1.0, 0.8, 0.64)
ax = sns.barplot(x=data['y'], y=data['x'] ,orient='h', color= light_orange, width=0.6)
ax.bar_label(ax.containers[0], labels= ['100,00','1001','909,9091,109'], fontsize=50)
plt.box(False)
ax.set_xlabel('', visible=False)
ax.tick_params(axis='y', which='major', labelsize=65)
ax.tick_params(axis='x', which='major', labelsize=50)
plt.yticks(fontname=font)
ax.set_ylabel('', visible=False)
#plt.rc('axes', labelsize=5)
plt.xticks(list(range(0,total-5,int(0.2*total))),[str(x)+'%' for x in list(range(0,100,20))])
plt.savefig(f'./Visualizations/dummy1.png', dpi=300, bbox_inches='tight')


fig, ax = plt.subplots(figsize=(70,15))
ax1 = sns.barplot(x='y', y='x', data=data,color=blue, lw =0, width=0.6)
sns.barplot(x='a', y='x', data=data,color=light_orange, lw =0, width=0.6)
ax.tick_params(axis='y', which='major', labelsize=65)
ax.tick_params(axis='x', which='major', labelsize=50)
plt.yticks(fontname=font)
plt.xticks(list(range(-30,30,6)), [str(i) + '%' for i in range(-30,30,6)])
ax.set_xlabel('', visible=False)
plt.box(False)
colors = {'Y': blue, 'A':  light_orange}
labels = list(colors.keys())
handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) for label in labels]
plt.legend(handles, labels, fontsize=50)
# set the chart title
# show the chart
plt.savefig(f'./Visualizations/dummy2.png')

c.drawImage('./Visualizations/dummy1.png', 20, 625, 200,105)
c.drawImage('./Visualizations/dummy2.png', 20, 395, 450,220)
data = [
    ["Name", "Age"],
    ["John", "25"],
    ["Jane", "30"]
]

from reportlab.lib import colors
df = housing_affordability('Champaign County')
# Set table style
style = [
    ('BACKGROUND', (0, 0), (-1, 0), colors.white),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ('TEXTCOLOR', (-1, 0), (-1, -1), colors.grey),
    ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ('LINEBELOW', (0, 0), (-1, -2), 1, colors.black),
    ('LINEAFTER', (0,0), (-2, -1), 1, colors.black),
]

# Create a table object
df = df.astype(str)
#table = [data[0]] + [map(str, row) for row in data[1:]]
col = df.columns.tolist()
x = df[df.columns].values.tolist()
x_ = [map(str, p) for p in x]
table = [col] + x_
print(table)
#exit()
df_table = [list(df.iloc[[i]]) for i in range(0, len(df))]
table_formatted = Table(table)
table_formatted.setStyle(style)

# Draw the table on the canvas
table_formatted.wrapOn(c, inch * 5, inch * 1)
table_formatted.drawOn(c, inch * 2, inch * 2)

# Save the PDF file
c.save()
#c.save()
