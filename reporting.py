"""
Script to automate reports given a template for all counties in Illinois for the ISDC project.

Author: Pranav Sekhar
Date: 14th feb. 2023
"""

import fpdf
import numpy as np
from fpdf import FPDF
import time
import pandas as pd
import matplotlib.pyplot as plt
import dataframe_image as dfi

input_df = pd.read_csv('./Data/B01001_county.csv')
input_df = input_df[['NAME', 'Estimate!!Total:!!Female:', 'Estimate!!Total:!!Male:','Estimate!!Total:!!Male:!!15 to 17 years', 'Estimate!!Total:!!Female:!!15 to 17 years']]
totals = [np.sum(input_df['Estimate!!Total:!!Female:']), np.sum(input_df['Estimate!!Total:!!Male:'])]
input_df.columns = ['County_name', 'Total_Females', 'Total_Males', 'Male_15_to_17_years', 'Female_15_to_17_years']
input_df['Female_pct'] = input_df['Female_15_to_17_years']/input_df['Total_Females']
input_df['Male_pct'] = input_df['Male_15_to_17_years']/input_df['Total_Males']
styled_df = input_df.head(10).style.hide_index().bar(subset=['Male_pct','Female_pct'], color='green')
dfi.export(styled_df,'./Data/Styled.png')
y_pos = np.arange(len(['Female','Male']))
plt.bar(y_pos, totals)

plt.xticks(y_pos, ['Female','Male'])
plt.savefig('./Data/totals.png')


class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297

    def footer(self):
        # Page numbers in the footer
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def page_body(self, images):
        # Determine how many plots there are per page and set positions
        # and margins accordingly
        if len(images) == 3:
            self.image(images[0], 15, 25, self.WIDTH - 30)
            self.image(images[1], 15, self.WIDTH / 2 + 5, self.WIDTH - 30)
            self.image(images[2], 15, self.WIDTH / 2 + 90, self.WIDTH - 30)
        elif len(images) == 2:

            self.image(images[0], 15, 25, self.WIDTH - 30)
            self.image(images[1], 15, self.WIDTH / 2 + 5, self.WIDTH - 30)
        else:
            print(images)
            self.image(images, 15, 25, self.WIDTH - 30)

    def print_page(self, images, counter):
        # Generates the report
        if counter ==0 :
            self.add_page()
        self.page_body(images)


pdf = PDF()
plots_per_page = ['Data/totals.png','Data/Styled.png']
counter =0

for elem in plots_per_page:
    pdf.print_page(elem, counter)
    counter += 1

pdf.output('PopulationReport.pdf', 'F')


