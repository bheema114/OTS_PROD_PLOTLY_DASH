import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import cx_Oracle
import json
import cachetools
import redis

# Initialize Oracle client
cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_19_18")

# Load configuration
config = json.load(open('config.yaml'))
db_username = config['db_username']
db_password = config['db_password']
db_host = config['db_host']
db_port = config['db_port']
db_service = config['db_service']

# Connect to the database
dsn = cx_Oracle.makedsn(db_host, db_port, service_name=db_service)
connection = cx_Oracle.connect(db_username, db_password, dsn=dsn)

# Execute SQL queries
sqlcursor = connection.cursor()
query_list = ['Revenue_Cash_NonCash.sql', 'Revenue_Cash.sql', 'Revenue_NonCash.sql']
dfs = {}
for query in query_list:
    with open(query, 'r') as file:
        sql_script = file.read()

    sql_statements = sql_script.split(';')

    # Execute each SQL statement
    for statement in sql_statements:
        if statement.strip():
            sqlcursor.execute(statement)

    result = sqlcursor.fetchall()
    if query == query_list[0]:
        dfs['CashNonCash'] = pd.DataFrame(result, columns=["transaction_date",
                                                "mid", "station_name",
                                                "transactiontype",
                                                "equipment_id",
                                                "payment_type",
                                                "payment_type_name",
                                                "transaction_count",
                                                "income",
                                                "outgoing",
                                                "total"
                                                ])
    elif query == query_list[1]:
        dfs['Cash'] = pd.DataFrame(result, columns=["transaction_date",
                                              "mid", "station_name",
                                              "transactiontype",
                                              "equipment_id",
                                              "payment_type",
                                              "payment_type_name",
                                              "transaction_count",
                                              "income",
                                              "outgoing",
                                              "total"
                                              ])
    else:
        dfs['NonCash'] = pd.DataFrame(result, columns=["transaction_date",
                                               "mid", "station_name",
                                               "transactiontype",
                                               "equipment_id",
                                               "payment_type",
                                               "payment_type_name",
                                               "transaction_count",
                                               "income",
                                               "outgoing",
                                               "total"
                                               ])
# Close the database connection
sqlcursor.close()
connection.close()

# Renaming columns for easier access
for key in dfs.keys():
    dfs[key].columns = ["Date", "MID", "Station", "Transaction Type", "Equipment ID", "Payment Type", "Payment Type Name",
                        "Transaction Count", "Incoming", "Outgoing", "Revenue"]

# Converting the 'Date' column to datetime
for key in dfs.keys():
    dfs[key]['Date'] = pd.to_datetime(dfs[key]['Date'])

# Connect to Redis
#redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Create a cache using cachetools and Redis
#cache = cachetools.TTLCache(maxsize=100, ttl=3600)  # Cache for 1 hour

# Define Dash app
app = dash.Dash(external_stylesheets=[dbc.themes.GRID])
server = app.server

# Define y-axis and x-axis value options
y_axis_options = ['Incoming', 'Outgoing', 'Revenue']  
x_axis_options = ['Station',"Transaction Type", "Equipment ID","Payment Type Name"]  

# Define app layout
# app.layout = html.Div(
#     [
#         dbc.Row(
#             dbc.Col(
#                 html.Div("A single, half-width column"),
#                 width={"size": 6, "offset": 3},
#             )
#         ),
#         dbc.Row(
#             [
#                 dbc.Col(
#                     html.Div("The last of three columns"),
#                     width={"size": 3, "order": "last", "offset": 1},
#                 ),
#                 dbc.Col(
#                     html.Div("The first of three columns"),
#                     width={"size": 3, "order": 1, "offset": 2},
#                 ),
#                 dbc.Col(
#                     html.Div("The second of three columns"),
#                     width={"size": 3, "order": 5},
#                 ),
#             ]
#         ),
#     ]
# )
app.layout = html.Div([
    dbc.Row([
        dbc.Col(html.Div(html.Label('Date Range:')),width="auto"),
        dbc.Col(html.Div(html.Label('Station:')),width="auto"),
        dbc.Col(html.Div(html.Label('Equipment ID:')),width="auto"),
        dbc.Col(html.Div(html.Label('Payment Category:')),width="auto"),
        dbc.Col(html.Div(html.Label('Transaction Type:')),width="auto"),
        
    ]),

    dbc.Row([
        dbc.Col(html.Div(
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=dfs['Cash']['Date'].min(),
                end_date=dfs['Cash']['Date'].max(),
                display_format='YYYY-MM-DD'
            ),
            #style={'width': '48%', 'display': 'inline-block'}
        ),width=2),

        dbc.Col(html.Div(
            dcc.Dropdown(
                id='station-id-dropdown',
                options=[
                    {'label': 'All Station', 'value': 'All'}
                ] + [
                    {'label': station, 'value': station} for station in dfs['Cash']['Station'].unique()
                ],
                value='All',
                
            ),
            style={'width': 200, 'display': 'inline-block'}
        ),
        width=2),
    #], className='mb-2'),

    dbc.Col(html.Div(
            dcc.Dropdown(
                id='equipment-id-dropdown',
                options=[
                    {'label': 'All Equipment', 'value': 'All'}
                ] + [
                    {'label': equipment_id, 'value': equipment_id} for equipment_id in dfs['Cash']['Equipment ID'].unique()
                ],
                value='All',
            ),
            style={'width': 200, 'display': 'inline-block'}
        ),width=2),
    #], className='mb-2'),

   dbc.Col(html.Div(
            dcc.Dropdown(
                id='payment-category-dropdown',
                options=[
                    {'label': 'Cash', 'value': 'Cash'},
                    {'label': 'NonCash', 'value': 'NonCash'},
                    {'label': 'CashNonCash', 'value': 'CashNonCash'}
                ],
                value='CashNonCash',
                style={'width': 200, 'display': 'inline-block'}
            )),
            width=2
        ),
    #], className='mb-2'),

    dbc.Col(html.Div(
            dcc.Dropdown(
                id='transaction-type-dropdown',
                options=[
                    {'label': 'All Transaction Types', 'value': 'All'},
                    {'label': '4-Add Value', 'value': '4-Add Value'},
                    {'label': '9-Admin Handling', 'value': '9-Admin Handling'}
                ],
                value='All',
                style={'width': 200, 'display': 'inline-block'}
            )),
            width=2
        ),
    
    ], className='mb-2'),

    dbc.Row([
        dbc.Col(html.Div(html.Label('Y-Axis Value:')),width="auto"),
        dbc.Col(html.Div(
            dcc.RadioItems(
                id='y-axis-radio',
                options=[
                    {'label': y_value, 'value': y_value} for y_value in y_axis_options
                ],
                value='Revenue',
                labelStyle={'display': 'block', 'margin-bottom': '10px'},
                style={'display': 'inline-block'}
            )),
            width=2
        ),
    ], className='mb-2'),

    dbc.Row([
        dbc.Col(html.Div(html.Label('X-Axis Value:')),width="auto"),
        dbc.Col(html.Div(
            dcc.RadioItems(
                id='x-axis-radio',
                options=[
                    {'label': x_value, 'value': x_value} for x_value in x_axis_options
                ],
                value='Station',
                labelStyle={'display': 'block', 'margin-bottom': '10px'},
                style={'display': 'inline-block'},
                inline=True
            )),
            width=2
        ),
    ], className='mb-2'),

    dbc.Row([
        dbc.Col(dcc.Graph(id='revenue-graph')),
    ]),
    
     dbc.Row([
        dbc.Col(html.Div(id='total-revenue-scorecard')),
        dbc.Col(html.Div(id='incoming-scorecard')),
        dbc.Col(html.Div(id='outgoing-scorecard')),
    ]),
    
    dcc.Interval(
        id='update-interval',
        interval=60*1000,  # Update every minute (adjust as needed)
        n_intervals=0
    ),
])


# Define callback to update graph
@app.callback(
    [Output('revenue-graph', 'figure'),
    Output('total-revenue-scorecard', 'children'),
    Output('incoming-scorecard', 'children'),
    Output('outgoing-scorecard', 'children')],
    [Input('update-interval', 'n_intervals'),
    Input('payment-category-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('equipment-id-dropdown', 'value'),
     Input('station-id-dropdown', 'value'),
     Input('transaction-type-dropdown', 'value'),
     Input('x-axis-radio', 'value'),
     Input('y-axis-radio', 'value')]  # Use radio items for y-axis selection
)

def update_graph(n,payment_mode, start_date, end_date, equipment_id, selected_station, transaction_type, x_axis_value, y_axis_value):
    # Calculate the current total revenue, incoming, and outgoing values
    total_revenue = dfs['CashNonCash']['Revenue'].sum()
    incoming = dfs['CashNonCash']['Incoming'].sum()
    outgoing = dfs['CashNonCash']['Outgoing'].sum()

    # You can format the values as needed, e.g., using f-strings
    total_revenue_formatted = f'Total Revenue: ${total_revenue:,.2f}'
    incoming_formatted = f'Incoming: ${incoming:,.2f}'
    outgoing_formatted = f'Outgoing: ${outgoing:,.2f}'
    
        
    df = dfs[payment_mode]

    # Convert selected transaction_type to lowercase for case-insensitive comparison
    transaction_type = transaction_type.lower()

    if equipment_id == 'All':
        filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    else:
        filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date) & (df['Equipment ID'] == equipment_id)]

    if selected_station != 'All':
        filtered_df = filtered_df[filtered_df['Station'] == selected_station]

    if transaction_type != 'all':
        # Convert Transaction Type column to lowercase for case-insensitive comparison
        transaction_type = transaction_type.lower()
        filtered_df = filtered_df[filtered_df['Transaction Type'].str.lower() == transaction_type]

    fig = go.Figure()

    for x_value in filtered_df[x_axis_value].unique():
        x_df = filtered_df[filtered_df[x_axis_value] == x_value]

        # Calculate the aggregated value based on the selected y-axis value
        aggregated_value = x_df[y_axis_value].sum()

        fig.add_trace(go.Bar(
            x=[x_value],
            y=[aggregated_value],
            name=x_value,
            text=[aggregated_value],
            textposition='auto'
        ))

    fig.update_layout(
        title=f'Revenue vs {x_axis_value} ({y_axis_value} on y-axis)',
        xaxis_title=x_axis_value,
        yaxis_title=y_axis_value,
        bargap=0.2,
        bargroupgap=0.1,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Arial, monospace",
            size=14,
            color="black"
        ),
        margin=dict(l=50, r=50, b=50, t=50),
        xaxis=dict(showline=True, showgrid=False, linecolor='rgb(204, 204, 204)'),
        yaxis=dict(showline=True, showgrid=False, linecolor='rgb(204, 204, 204)')
    )

    return total_revenue_formatted, incoming_formatted, outgoing_formatted,fig

if __name__ == '__main__':
    app.run_server(debug=True)
