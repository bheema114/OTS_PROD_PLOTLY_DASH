import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
from data import dfr
from datetime import datetime

dash.register_page(__name__, path='/ridership', name="Ridership")

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
    ], className='input-wrapper'),

    dcc.Graph(id='ridership-graph',
              config={
                  "displaylogo": False,
                  'modeBarButtonsToRemove': ['pan2d', 'lasso2d']
              })
])


@callback(
    Output('ridership-graph', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('station-id-dropdown', 'value')]
)
def update_graph(start_date, end_date, selected_station):
    # Filter data based on selected filters
    # Assuming the Ridership DataFrame is nested within 'Ridership' key
    ridership_df = dfr['Ridership']

    filtered_df = ridership_df[(ridership_df['Date'] >= start_date) & (
        ridership_df['Date'] <= end_date)]

    if selected_station != 'All':
        filtered_df = filtered_df[filtered_df['Station'] == selected_station]

    fig = go.Figure()

    x_values = ['Entry Count', 'Exit Count']
    y_values = [filtered_df['Entry Count'].sum(
    ), filtered_df['Exit Count'].sum()]

    fig.add_trace(go.Bar(
        x=x_values,
        y=y_values,
        text=y_values,
        textposition='auto',
        hoverinfo='text+name',
        marker_color=['blue', 'green'],
        name='Count'
    ))

    fig.update_layout(
        title=f'Ridership (Entry/Exit Count)',
        xaxis_title='Category',
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
                   linecolor='rgb(204, 204, 204)'),
        yaxis=dict(showline=True, showgrid=False,
                   linecolor='rgb(204, 204, 204)')
    )

    return fig
