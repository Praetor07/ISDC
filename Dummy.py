import pandas as pd
import plotly.graph_objects as gp
import matplotlib.pyplot as plt
import plotly

dataframe = pd.read_csv('/Users/pranavsekhar/PycharmProjects/ISDC/Data/Population_by_age_county.csv')
dataframe = dataframe[dataframe['NAME'] == 'Champaign County']
dataframe = dataframe[dataframe.columns[6:]]
pivot_df = dataframe.T
pivot_df.reset_index(inplace=True)
pivot_df.columns = ['Ages', 'Male', 'Female']
pivot_df.drop([0,1], axis = 0, inplace = True)

y_age = pivot_df['Ages']
x_M = pivot_df['Male']
x_F = pivot_df['Female'] * -1
fig = gp.Figure()

# Adding Male data to the figure
fig.add_trace(gp.Bar(y= y_age, x = x_M,
                     name = 'Male',
                     orientation = 'h'))

# Adding Female data to the figure
fig.add_trace(gp.Bar(y = y_age, x = x_F,
                     name = 'Female', orientation = 'h'))

# Updating the layout for our graph
fig.update_layout(title = 'Population Pyramid of Champaign County-2021',
                 title_font_size = 22, barmode = 'relative',
                 bargap = 0.0, bargroupgap = 0,
                 xaxis = dict(tickvals = [-60000000, -40000000, -20000000,
                                          0, 20000000, 40000000, 60000000],

                              ticktext = ['6M', '4M', '2M', '0',
                                          '2M', '4M', '6M'],

                              title = 'Population by Age',
                              title_font_size = 14)
                 )

#fig.show()
fig.write_image('PopPyramid2.png')