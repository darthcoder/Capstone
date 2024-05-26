import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # TASK 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()] + [{'label': 'All Sites', 'value': 'ALL'}],
        value='ALL',
        placeholder='Select a Launch Site here',
        searchable=True
    ),

    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    dcc.Graph(id='success-pie-chart'),

    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[min_payload, max_payload]
    ),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    dcc.Graph(id='success-payload-scatter-chart'),
])

# TASK 2: Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Filter data for all sites
        filtered_df = spacex_df
        fig = px.pie(filtered_df, names='class', 
                     title='Total Success Launches by Site')
        return fig
    else:
        # Filter data for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        
        # Count the successful and failed launches
        success_count = filtered_df[filtered_df['class'] == 1].shape[0]
        failed_count = filtered_df[filtered_df['class'] == 0].shape[0]
        
        # Create the pie chart
        values = [success_count, failed_count]
        names = ['Success', 'Failed']
        fig = px.pie(values=values, names=names, 
                     title=f'Success vs Failed Launches for {entered_site}')
        return fig

# TASK 4: Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def get_scatter_chart(entered_site, payload_range):
    filtered_df = spacex_df
    
    # Filter the data based on the selected site
    if entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
    
    # Filter the data based on the selected payload range
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload_range[0]) & (filtered_df['Payload Mass (kg)'] <= payload_range[1])]
    
    # Create the scatter plot
    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Correlation between Payload and Launch Success'
    )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()