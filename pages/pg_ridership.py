import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
from data import dfr

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



layout = html.Div([
    html.Link(rel='stylesheet', href='/assets/ots_styles.css'),
    dbc.Row([
        dbc.Col([
            html.Label('Date Range:')],
            className="hstack gap-2 label", width=2
        ),
        dbc.Col([
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=dfr['Ridership']['Date'].min(),
                end_date=dfr['Ridership']['Date'].max(),
                display_format='YYYY-MM-DD'
            )
        ], className='hstack', width=4),
        dbc.Col([
            html.Label('Station:', style={'text-align': 'left', 'color': '#2b3674', 'font-weight': 'bold'})
        ], className="hstack", width=1),
        dbc.Col([
            dcc.Dropdown(
                id='station-id-dropdown',
                options=[
                    {'label': 'All Station', 'value': 'All'}
                ] + [
                    {'label': station, 'value': station} for station in dfr['Ridership']['Station'].unique()
                ],
                value='All',
                style={'width': '150%', 'justify-content': 'center', 'marginRight': '80px'}
            )
        ], width={'size': 2}, className="hstack gap-2"),
    ], className='p-2 align-items-center date-range hstack gap-2'),
   
    dcc.Graph(id='ridership-graph',
              config={
        "displaylogo": False,
        'modeBarButtonsToRemove': ['pan2d','lasso2d']
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
    ridership_df = dfr['Ridership']  # Assuming the Ridership DataFrame is nested within 'Ridership' key

    filtered_df = ridership_df[(ridership_df['Date'] >= start_date) & (ridership_df['Date'] <= end_date)]

    if selected_station != 'All':
        filtered_df = filtered_df[filtered_df['Station'] == selected_station]

    fig = go.Figure()

    x_values = ['Entry Count', 'Exit Count']
    y_values = [filtered_df['Entry Count'].sum(), filtered_df['Exit Count'].sum()]

    fig.add_trace(go.Bar(
        x=x_values,
        y=y_values,
        text=y_values,
        textposition='auto',
        hoverinfo='text+name',
        marker_color=['blue', 'green']
    ))

    fig.update_layout(
        title=f'Ridership (Count on y-axis)',
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
        xaxis=dict(showline=True, showgrid=False, linecolor='rgb(204, 204, 204)'),
        yaxis=dict(showline=True, showgrid=False, linecolor='rgb(204, 204, 204)')
    )

    return fig

