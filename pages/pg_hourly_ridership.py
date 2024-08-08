import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
from data import dfr
from datetime import datetime
from dash.exceptions import PreventUpdate

dash.register_page(__name__, path='/hourly', name="Hourly Ridership")

# Renaming columns for easier access
for key in dfr.keys():
    dfr[key].columns = ['Station',
                        'Equip Grp ID',
                        'Equip ID',
                        'Exit Count',
                        'Exit TRX DATE',
                        'Entry Count',
                        'Entry TRX DATE',
                        'TRX TYPE',
                        'TRX SEQ NUM',
                        'LINE ID',
                        'AQUIRER ID',
                        'OPERATOR ID',
                        'TERMINAL ID',
                        'CARD TYPE',
                        'PANSHA',
                        'PRODUCT TYPE',
                        'TRX AMOUNT',
                        'CARD BALANCE',
                        'PAYTM TID',
                        'PAYTM MID',
                        'Date']

# Converting the 'Date' column to datetime
for key in dfr.keys():
    dfr[key]['Date'] = pd.to_datetime(dfr[key]['Date'])


today_date = datetime.today().strftime('%Y-%m-%d')

layout = html.Div([
    html.Link(rel='stylesheet', href='/assets/ots_styles.css'),
    dbc.Row([

        dbc.Col(
            html.Div([
                html.Label('Date Range', className='custom-label'),
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date=today_date,
                    end_date=today_date,
                    display_format='YYYY-MM-DD',
                ),
            ]),  sm=12, md=6, lg=3,
        ),

        dbc.Col(
            html.Div([
                html.Label('Station', className='custom-label'),
                dcc.Dropdown(
                    id='station-id-dropdown',
                    options=[
                        {'label': 'All Station', 'value': 'All'}
                    ] + [
                        {'label': station, 'value': station} for station in dfr['Ridership']['Station'].unique()
                    ],
                    value='All',
                ),
            ]),   sm=12, md=6, lg=3,
        ),

        dbc.Col(
            html.Div([
                html.Label('Equipment ID', className='custom-label'),
                dcc.Dropdown(
                    id='Equipment-id-dropdown',
                    options=[
                        {'label': 'All Equipment', 'value': 'All'}
                    ] + [
                        {'label': EquipID, 'value': EquipID} for EquipID in dfr['Ridership']['Equip ID'].unique()
                    ],
                    value='All',
                ),
            ]),  sm=12, md=6, lg=3,
        ),

    ], className='input-wrapper'),


    dcc.Graph(id='Hridership-graph',
              config={
                  "displaylogo": False,
                  'modeBarButtonsToRemove': ['pan2d', 'lasso2d']
              })
])


@callback(
    Output('Hridership-graph', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('station-id-dropdown', 'value'),
     Input('Equipment-id-dropdown', 'value')]
)
def update_graph(start_date, end_date, selected_station, selected_equipment):

    # if start_date is None or end_date is None:
    #     raise PreventUpdate("Please select valid start and end dates.")

    # if start_date > end_date:
    #     raise PreventUpdate("Start date must be before or equal to end date.")

    # Filter data based on selected filters
    ridership_df = dfr['Ridership']

    # ridership_df['Date'] = pd.to_datetime(ridership_df['Date'])

    filtered_df = ridership_df[(ridership_df['Date'] >= start_date) & (
        ridership_df['Date'] <= end_date)]

    if selected_station != 'All':
        filtered_df = filtered_df[filtered_df['Station'] == selected_station]

    if selected_equipment != 'All':
        filtered_df = filtered_df[filtered_df['Equip ID']
                                  == selected_equipment]

    # Group data by hour and calculate the sum of entry count and exit count
    grouped_df = filtered_df.groupby(filtered_df['Date'].dt.hour)[
        ['Entry Count', 'Exit Count']].sum()

    fig = go.Figure()

    # Add traces for entry count and exit count
    fig.add_trace(go.Bar(
        x=grouped_df.index,
        y=grouped_df['Entry Count'],
        name='Entry Count',
        text=grouped_df['Entry Count'],
        textposition='auto',
        hoverinfo='text+name',
        marker_color='blue'
    ))

    fig.add_trace(go.Bar(
        x=grouped_df.index,
        y=grouped_df['Exit Count'],
        name='Exit Count',
        text=grouped_df['Exit Count'],
        textposition='auto',
        hoverinfo='text+name',
        marker_color='orange'
    ))

    # Update layout and return the figure
    fig.update_layout(
        barmode='group',  # 'group' to group bars, 'stack' to stack bars
        title='Hourly Ridership (Entry Count and Exit Count)',
        xaxis_title='Hour',
        yaxis_title='Count',
        bargap=0.2,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Roboto",
            size=14,
            color="black"
        ),
        margin=dict(l=50, r=50, b=50, t=50),
        xaxis=dict(showline=True, showgrid=False,
                   linecolor='rgb(204, 204, 204)', dtick=1),
        yaxis=dict(showline=True, showgrid=False,
                   linecolor='rgb(204, 204, 204)')
    )

    return fig
