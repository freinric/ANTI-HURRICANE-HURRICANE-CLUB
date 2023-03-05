import pandas as pd     
import datetime as dt
import altair as alt

import dash                                     
from dash import dcc, html, Input, Output, html
import plotly.express as px
import dash_bootstrap_components as dbc

### TABLE OF CONTENTS ###
# DEFINING 'GLOBAL' VARIABLES
# PLOT FUNCTIONS
# APP LAYOUT
# CALLBACK

#------------------------------------------------------------------------------
# DEFINING
df = pd.read_csv("data/clean/mindata.csv")  

colors = {
    'background': '#6fa8dc',
    'background_dropdown': '#DDDDDD',
    'H1':'#c51b1b',
    'H2':'#7FDBFF',
    'H3':'#005AB5'
}


style_dropdown = {'width': '100%', 'font-family': 'arial', "font-size": "1.1em", "background-color": colors['background_dropdown'], 'font-weight': 'bold'}

style_H1 = {'textAlign': 'center', 'color': colors['H1']} # Title
style_H2 = {'textAlign': 'center', 'color': colors['H2']} # Subtitle
style_H3_c = {'textAlign': 'center', 'color': colors['H3'], 'width': '100%'} # For card
style_H3 = {'color': colors['H3'], 'width': '100%'} # For Charts Title

style_plot1 = {'border-width': '0', 'width': '100%', 'height': '970px'}
style_plot2 = {'border-width': '0', 'width': '100%', 'height': '400px'}
style_plot3 = {'border-width': '0', 'width': '100%', 'height': '400px'}

style_card = {'border': '1px solid #d3d3d3', 'border-radius': '10px'}

#------------------------------------------------------------------------------
### PLOT 1 FUNCTION ###
def plot_altair1(dff, drop1_chosen):
    barchart = alt.Chart(dff[-pd.isnull(dff[drop1_chosen])]).mark_bar().encode(
    alt.X(drop1_chosen, title='Count of '+ drop1_chosen, axis=alt.Axis(orient='top')),
    alt.Y('COUNTY', sort='-x', title=""),
    tooltip=[drop1_chosen,'COUNTY']).configure_axis(labelFontSize = 16, titleFontSize=20)
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
        x = alt.X(drop_a, axis=alt.Axis(format='.0f', title = None)),
        y = alt.Y('COUNTY', axis=alt.Axis(title = None))
        ).transform_filter(alt.FieldOneOfPredicate(field='COUNTY', oneOf=drop_b)
                           ).configure_axis(labelFontSize = 16)
    return chart.to_html()

### PLOT

#------------------------------------------------------------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

app.layout = dbc.Container([
       dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([html.H1('Social Vulnerability Indices in Puerto Rico', style = style_H1), 
                              html.H3('Which county needs the most help?', style = style_H2)]),
                color = colors['background']),
            html.Br(),
            
            ### CHECKLIST ###
            html.H3("Select Year: ", style = style_H3_c),
            dcc.Checklist(
                    id='year',                
                    options=[{'label': '2016', 'value': 2016, 'disabled':False}] +
                             [{'label': '2018', 'value': 2018, 'disabled':False}],
                    value=[2016],    # values chosen by default

                    ### STYLES IN CHECKLIST ###
                    className='my_box_container', 
                    inputClassName='my_box_input',         
                    labelClassName='my_box_label', 
                    inputStyle={"margin-right": "3px", "margin-left":"20px"},         
                ),
            html.Br(),
            
            ### SLIDER ###
            html.H3("Select County Population: ", style = style_H3_c),
            dcc.RangeSlider(id="population", min=1300, max=363744, step = 1000, 
                            marks={1300: '1.3k',
                                   50000: '50k',
                                   100000: '100k',
                                   363744: '364k'},
                            value=[1300,363744])], 
                            md = 3, style = style_card),
             
        ### PLOT 1 LAYOUT###    
        dbc.Col([
            dbc.Col([
                html.H3('Rank Counties by', style = style_H3), 
                ### DROPDOWN 1 ###
                dcc.Dropdown(
                    id='drop1',
                    placeholder="Variables",
                    value='E_TOTPOP',  
                    options=[{'label': col, 'value': col} for col in df.columns[1:19]], # only including actual variables
                    style = style_dropdown)], 
                    style = {'display': 'flex'}),
                html.Iframe(
                    id='plot1',
                    style = style_plot1)], 
            style={"height": "10%"}),

        ### PLOT 2  LAYOUT ###
        dbc.Col([
            dbc.Col([html.H3('Compare ', style = {'color': colors['H3']}),
                     dcc.Dropdown(
                                id='drop2_a',
                                value='E_UNEMP', 
                                options=[{'label': col, 'value': col} for col in df.columns[1:19]], 
                         style = style_dropdown),
                     html.H3('and ', style  = {'color': colors['H3']}),
                    dcc.Dropdown(
                        id='drop2_b',
                        value='E_TOTPOP', 
                        options=[{'label': col, 'value': col} for col in df.columns[1:19]], 
                        style =style_dropdown)], 
            style={'display':'flex'}),
            html.Iframe(
                id='plot2',
                style = style_plot2),
            html.Br(),
            
            ### PLOT 3 LAYOUT ###
            dbc.Col([html.H3('Compare', style = style_H3),
                     dcc.Dropdown(
                                id='drop3_a',
                                value='E_NOVEH', 
                                options=[{'label': col, 'value': col} for col in df.columns[1:19]], 
                                style=style_dropdown),
                     html.H3('among Counties', style = style_H3),
                     dcc.Dropdown(
                        id='drop3_b',
                        value=['Adjuntas', 'Aguada'], 
                        options=[{'label': counties, 'value': counties} for counties in df['COUNTY']], multi = True)],
                    style={'width': '100%', 'font-family': 'arial', "font-size": "1.1em", 'font-weight': 'bold'}),
            html.Iframe(
                id='plot3',
                style=style_plot3)
        ])
        ])
])

#------------------------------------------------------------------------------

### CALLBACK GRAPHS AND CHECKBOXES ###
@app.callback(
    Output(component_id='plot1', component_property='srcDoc'),
    Output(component_id='plot2', component_property='srcDoc'),
    Output(component_id='plot3', component_property='srcDoc'),
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
    dff = df[df['E_TOTPOP'].between(popmin, popmax)]

    # filter by year
    dff = dff[dff['year'].isin(options_chosen)]
    
    
    return (plot_altair1(dff, drop1_chosen), 
            plot_altair2(dff, drop2a_chosen, drop2b_chosen), 
            plot_altair3(dff, drop3a_chosen, drop3b_chosen),
            options_chosen)


#------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)