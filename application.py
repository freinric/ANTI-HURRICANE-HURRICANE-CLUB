import pandas as pd     
import datetime as dt
import altair as alt

import dash                                     
from dash import dcc, html, Input, Output, html
import plotly.express as px
import dash_bootstrap_components as dbc

### TABLE OF CONTENTS ###
# CREATE AND ENABLE ALTAIR THEME
# DEFINING 'GLOBAL' VARIABLES
# READ DATA
# PLOT FUNCTIONS
# APP LAYOUT
# CALLBACK

#------------------------------------------------------------------------------
# CREATE AND ENABLE ALTAIR THEME

alt.themes.enable('fivethirtyeight')

#------------------------------------------------------------------------------
# DEFINING
colors = {
    'background': '#6fa8dc',
    'background_dropdown': '#DDDDDD',
    'H1':'#000000',
    'H2':'#333333',
    'H3':'#333333'
}


style_dropdown = {'width': '100%', 'font-family': 'arial', "font-size": "1.1em", "background-color": colors['background_dropdown'], 'font-weight': 'bold'}

style_H1 = {'textAlign': 'left', 'color': colors['H1'], 'width' : 1520} # Title
style_H2 = {'textAlign': 'left', 'color': colors['H2'], 'width': 1520} # Subtitle
style_H3_c = {'textAlign': 'left', 'color': colors['H3'], 'fontSize': 24} # For Input
style_H3 = {'color': colors['H3'], 'width': '100%'} # For Charts Title

style_plot1 = {'border-width': '0', 'width': '100%', 'height': '450px'}
style_plot4 = {'border-width': '0', 'width': '100%', 'height': '450px'}
style_plot2 = {'border-width': '0', 'width': '100%', 'height': '450px'}
style_plot3 = {'border-width': '0', 'width': '100%', 'height': '450px'}

#------------------------------------------------------------------------------
# READ DATA

df = pd.read_csv("data/clean/mindata.csv")
df = df.rename(columns={df.columns[3]: "Total_Population", df.columns[4]: "Housing_units", df.columns[5]: "Households",
                        df.columns[6]: "Persons_below_poverty", df.columns[7]: "Unemployed_above_age16", df.columns[8]: "Per_capita_income",
                        df.columns[9]: "No_diploma_above_age25", df.columns[10]: "Above_age65", df.columns[11]: "Under_age17",
                        df.columns[12]: "population_disabled", df.columns[13]: "Single_parent_child_under_age18",df.columns[14]: "Minority_group", 
                        df.columns[15]: "Above_age5_belowavg_english", df.columns[16]: "Housing_10plus_units",df.columns[17]: "Mobile_homes", 
                        df.columns[18]: "More_people_than_rooms", df.columns[19]: "House_with_no_vehicle",df.columns[20]: "People_in_quarters",
                        df.columns[22]: "Socioeconomic", df.columns[23]: "Household Composition & Disability", df.columns[24]: "Minority Status & Language",
                        df.columns[25]: "Housing Type & Transportation"}) 

print(df.columns)
df2 = df.drop(columns=['Unnamed: 0.1', 'Unnamed: 0', 'year'])  

#------------------------------------------------------------------------------
### PLOT 1 FUNCTION ###
def plot_altair1(dff, drop1_chosen):
    barchart = alt.Chart(dff[-pd.isnull(dff[drop1_chosen])].sort_values(by=drop1_chosen, ascending=False).head(15)).mark_line().encode(
        alt.X(drop1_chosen,title=drop1_chosen),
        alt.Y('COUNTY', sort='-x', title='Top 10 Counties'),
        tooltip=[drop1_chosen,'COUNTY']
    ).configure_axis(
        labelFontSize=16,
        titleFontSize=20
    )
    return barchart.to_html()

### PLOT 2 FUNCTION ###
def plot_altair2(dff, drop_a, drop_b):
    chart = alt.Chart(dff).mark_circle(size = 100).encode(
        x= alt.X(drop_a, axis=alt.Axis(format='.0f')),
        y=alt.Y(drop_b, axis=alt.Axis(format='.0f')),
        tooltip=['COUNTY', drop_a, drop_b]
    ).configure_axis(labelFontSize = 16, titleFontSize=20)
    return chart.to_html()

### PLOT 3 FUNCTION ###
def plot_altair3(dff, drop_a, drop_b):  
    chart = alt.Chart(dff).mark_bar().encode(
        x = alt.X('COUNTY', sort='y', axis=alt.Axis(title = None)),
        y = alt.Y(drop_a, axis=alt.Axis(format='.0f'))
        ).transform_filter(alt.FieldOneOfPredicate(field='COUNTY', oneOf=drop_b)
                           ).configure_axis(labelFontSize = 16, titleFontSize=20)
    return chart.to_html()

### PLOT 4 FUNCTION ###
def plot_altair4(dff, drop1_chosen):
    barchart = alt.Chart(dff.sort_values(by=drop1_chosen, ascending=True).head(15)).mark_line().encode(
    alt.X(drop1_chosen, title=drop1_chosen),
    alt.Y('COUNTY', sort='x', title='Bottom 10 Counties'),
    tooltip=[drop1_chosen,'COUNTY']).configure_axis(labelFontSize = 16, titleFontSize=20)
    return barchart.to_html()

### PLOT

#------------------------------------------------------------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        dbc.Row(
            [
                # add title and subtitle
                html.H1('Social Vulnerability Indices in Puerto Rico', style = style_H1), 
                html.H3('Which county needs the most help?', style = style_H2),
                html.Br()
            ],
            style = {'background-color': '#FFFFFF'} 
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Br(),
                        html.H3("Select Year: ", style = style_H3_c),
                        dcc.RadioItems(
                                id='year',                
                                options=[{'label': '2016', 'value': 2016,}] +
                                        [{'label': '2018', 'value': 2018,}],
                                value=2016,    # values chosen by default

                                ### STYLES IN CHECKLIST ###
                                className='my_box_container', 
                                inputClassName='my_box_input',         
                                labelClassName='my_box_label', 
                                inputStyle={"margin-right": "3px", "margin-left":"20px"}),
                    
                        ### SLIDER ###
                        html.Br(),
                        html.H3("Select County Population: ", style = style_H3_c),
                        dcc.RangeSlider(id="population", min=1300, max=363744, step = 1000, 
                                        marks={1300: '1.3k',
                                            50000: '50k',
                                            100000: '100k',
                                            363744: '364k'},
                                        value=[1300,363744]),

                        ### DROPDOWN 1 ###
                        html.Br(),
                        html.Br(),
                        html.H3('Rank Counties by', style = style_H3_c), 
                        dcc.Dropdown(
                            id='drop1',
                            placeholder="Variables",
                            value='Socioeconomic',  
                            options=[{'label': 'Socioeconomic Status', 'value': 'Socioeconomic'},
                                     {'label': 'Household Composition & Disability', 'value': 'Household Composition & Disability'},
                                     {'label': 'Minority Status & Language', 'value': 'Minority Status & Language'},
                                     {'label': 'Housing Type & Transportation', 'value': 'Housing Type & Transportation'}], # only including actual variables
                            style = style_dropdown),
                        
                        ### DROPDOWN 2 ###
                        html.Br(),
                        html.Br(),
                        html.H3('Compare ', style = style_H3_c),
                        dcc.Dropdown(
                            id='drop2_a',
                            value='Unemployed_above_age16', 
                            options=[{'label': col, 'value': col} for col in df2.select_dtypes(include='number').columns], 
                            style = style_dropdown),

                        ### DROPDOWN 3 ###    
                        html.H3('VS', style  = style_H3_c),
                        dcc.Dropdown(
                            id='drop2_b',
                            value='Total_Population', 
                            options=[{'label': col, 'value': col} for col in df2.select_dtypes(include='number').columns], 
                            style =style_dropdown),
                        html.H3('in a Scatterplot', style = style_H3_c),
                        
                        ### DROPDOWN 4 ###
                        html.Br(),
                        html.Br(),
                        html.H3('Compare', style = style_H3_c),
                        dcc.Dropdown(
                            id='drop3_a',
                            value='House_with_no_vehicle', 
                            options=[{'label': col, 'value': col} for col in df2.select_dtypes(include='number').columns], 
                            style=style_dropdown),

                        ### DROPDOWN 5 ###
                        html.H3('Among Counties', style = style_H3_c),
                        dcc.Dropdown(
                            id='drop3_b',
                            value=df.head(15)['COUNTY'], 
                            options=[{'label': counties, 'value': counties} for counties in df['COUNTY']], multi = True),
                        html.H3('in a Barplot', style = style_H3_c)
                    ],
                    style = {'background-color': '#FFFFFF'},
                    width = 2
                ),
                dbc.Col(width = 1),
                dbc.Col(
                    [
                        ### PLOT 1 LAYOUT###    
                        html.Iframe(
                            id='plot1',
                            style = style_plot1),

                        ### PLOT 4 LAYOUT ###
                        html.Iframe(
                            id='plot4',
                            style = style_plot1)
                    ],
                    style = {'background-color': '#FFFFFF'},
                    width = 4
                ),
                dbc.Col(width = 1),
                dbc.Col(
                    [
                        dbc.Row(
                            dbc.Col(
                                [
                                    
                                    ### PLOT 2 LAYOUT ###
                                    html.Iframe(
                                        id='plot2',
                                        style = style_plot2)                                      
                                ],
                                style = {'background-color': '#FFFFFF'}
                            )
                        ),
                        dbc.Row(
                            dbc.Col(
                                [
                                    
                                    ### PLOT 3 LAYOUT ###
                                    html.Iframe(
                                        id='plot3',
                                        style=style_plot3)
                                ],
                                style = {'background-color': '#FFFFFF'},
                            )
                        )
                    ],
                    width = 4
                )
            ]
        )
    ]
)

#------------------------------------------------------------------------------

### CALLBACK GRAPHS AND CHECKBOXES ###
@app.callback(
    Output(component_id='plot1', component_property='srcDoc'),
    Output(component_id='plot2', component_property='srcDoc'),
    Output(component_id='plot3', component_property='srcDoc'),
    Output(component_id='plot4', component_property='srcDoc'),
    Output('year', 'value'),
    [Input(component_id='year', component_property='value'),
     Input('population', 'value'),
     Input('drop1', 'value'),
     Input('drop2_a', 'value'),
     Input('drop2_b', 'value'),
     Input('drop3_a', 'value'),
     Input('drop3_b', 'value'),
     ]
)
def update_df(options_chosen, population_chosen, 
              drop1_chosen, 
              drop2a_chosen, drop2b_chosen, 
              drop3a_chosen, drop3b_chosen):

    # filter by population
    popmin = population_chosen[0]
    popmax = population_chosen[1]
    dff = df[df['Total_Population'].between(popmin, popmax)]

    # filter by year
    dff = dff[dff['year'] == options_chosen]
    
    
    return (plot_altair1(dff, drop1_chosen), 
            plot_altair2(dff, drop2a_chosen, drop2b_chosen), 
            plot_altair3(dff, drop3a_chosen, drop3b_chosen),
            plot_altair4(dff, drop1_chosen),
            options_chosen)

application = app.server

#------------------------------------------------------------------------------
if __name__ == '__main__':
    application.run(host='0.0.0.0', port='8080')