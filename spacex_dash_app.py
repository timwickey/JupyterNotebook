# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Unique launch sites in the dataframe
launch_sites = spacex_df['Launch Site'].unique().tolist()
# Options for dropdown
dropdown_options = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in launch_sites]


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),


                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                dcc.Dropdown(id='site-dropdown', options=dropdown_options, value='ALL', placeholder="Select a Launch Site here", searchable=True),
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                # TASK 3: Add a slider to select payload range
                                html.P("Payload range (Kg):"),
                                    dcc.RangeSlider(id='payload-slider',
                                                    min=0,
                                                    max=10000,
                                                    step=1000,
                                                    marks={i: '{}'.format(i) for i in range(0, 10001, 1000)},
                                                    value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Use all rows in the dataframe to render and return a pie chart graph
        fig = px.pie(spacex_df, names='class', title='Total Success Launches for All Sites')
    else:
        # Filter the dataframe for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Render and return a pie chart graph to show success and failure counts
        fig = px.pie(filtered_df, names='class', title=f'Total Success Launches for site {entered_site}')
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id="payload-slider", component_property="value")]
)
def update_scatter(selected_site, payload_range):
    # Filtering based on the selected site
    if selected_site == 'ALL':
        filtered_df = spacex_df
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
    
    # Further filter based on the payload range
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload_range[0]) & (filtered_df['Payload Mass (kg)'] <= payload_range[1])]

    # Create a scatter plot
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', 
                     title=f'Success by Payload for {selected_site}', labels={'class': 'Launch Outcome'})
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
