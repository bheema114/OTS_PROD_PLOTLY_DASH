import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import cx_Oracle
import json

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

# Define Dash app
app = dash.Dash(__name__)
server = app.server
app.server.static_folder = 'assets'


# Define y-axis and x-axis value options
y_axis_options = ['Incoming', 'Outgoing', 'Revenue']  
x_axis_options = ['Station',"Transaction Type", "Equipment ID","Payment Type Name"]  

# Define app layout
app.layout = html.Div([
    html.Link(rel='stylesheet', href='/assets/bootstrap.min.css'),
    html.Link(rel='stylesheet', href='/assets/style.css'),
    html.Link(rel='stylesheet', href='/assets/s1.css'),

#ROW1
  dbc.Row([
        dbc.Col([
            html.Label('Date Range:', style={'text-align': 'left','color': 'blue','font-weight':'bold','marginLeft':'50px'}),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=dfs['Cash']['Date'].min(),
                end_date=dfs['Cash']['Date'].max(),
                display_format='YYYY-MM-DD',
                style={'width': '200%','marginRight':'80px'}
            ),
             ],width={'size': 8, 'offset': 0, 'order': 1}, className="hstack gap-2"),
      ],className='p-2 align-items-center'),
      
#ROW2       
dbc.Row([

        dbc.Col([
            html.Label('Station:',style={'text-align': 'left', 'color': 'blue', 'font-weight': 'bold', 'marginLeft': '50px'}),
            dcc.Dropdown(
                id='station-id-dropdown',
                options=[
                    {'label': 'All Station', 'value': 'All'}
                ] + [
                    {'label': station, 'value': station} for station in dfs['Cash']['Station'].unique()
                ],
                value='All',
                style={'width': '150%','justify-content': 'center','marginRight':'80px'}
            ),
            ],width={'size': 3, 'offset': 0, 'order': 2}, className="hstack gap-2"),
    

        dbc.Col([
            html.Label('Equipment ID:',style={'text-align': 'left', 'color': 'blue', 'font-weight': 'bold', 'marginLeft': '50px'}),
            dcc.Dropdown(
                id='equipment-id-dropdown',
                options=[
                    {'label': 'All Equipment', 'value': 'All'}
                ] + [
                    {'label': equipment_id, 'value': equipment_id} for equipment_id in dfs['Cash']['Equipment ID'].unique()
                ],
                value='All',
                style={'width': '150%','justify-content': 'center','marginRight':'80px'}
            ),
            ],width={'size': 3, 'offset': 0, 'order': 2}, className="hstack gap-2"),
     

        dbc.Col([
            html.Label('Payment Category:',style={'text-align': 'left', 'color': 'blue', 'font-weight': 'bold', 'marginLeft': '50px'}),
            dcc.Dropdown(
                id='payment-category-dropdown',
                options=[
                    {'label': 'Cash', 'value': 'Cash'},
                    {'label': 'NonCash', 'value': 'NonCash'},
                    {'label': 'CashNonCash', 'value': 'CashNonCash'}
                ],
                value='CashNonCash',
                style={'width': '150%','justify-content': 'center','marginRight':'80px'}
            ),
            ],width={'size': 3, 'offset': 0, 'order': 2}, className="hstack gap-2"),
        

        dbc.Col([
            html.Label('Transaction Type:',style={'text-align': 'left', 'color': 'blue', 'font-weight': 'bold', 'marginLeft': '50px'}),
            dcc.Dropdown(
                id='transaction-type-dropdown',
                options=[
                    {'label': 'All Transaction Types', 'value': 'All'},
                    {'label': '4-Add Value', 'value': '4-Add Value'},
                    {'label': '9-Admin Handling', 'value': '9-Admin Handling'}
                ],
                value='All',
                style={'width': '150%','justify-content': 'center','marginRight':'80px'}
            ),
            ],width={'size': 3, 'offset': 0, 'order': 2}, className="hstack gap-2"),
    
        ],className='p-2 align-items-center'),

#ROW3
dbc.Row([
     dbc.Col([
        html.Label('X-Axis Value:',style={'text-align': 'left' ,'color': 'blue', 'font-weight': 'bold', 'marginLeft': '50px'}),
        dbc.RadioItems(
            id='x-axis-radio',
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-info",
            labelCheckedClassName="active",
            options=[
                {'label': x_value, 'value': x_value} for x_value in x_axis_options
            ],
            value='Station',
            labelStyle={'white-space': 'pre-wrap'}
            #style={'width': '75%','justify-content': 'center'}
            
        ),
        ],width={'size': 8, 'offset': 0, 'order': 2}, className="hstack gap-2" "radiobutton-group"),
        ],className='p-2 align-items-center'),
    dbc.Row([
    dbc.Col([
        html.Label('Y-Axis Value:',style={'text-align': 'left','color': 'blue', 'font-weight': 'bold', 'marginLeft': '50px',}),
        dbc.RadioItems(
            id='y-axis-radio',
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-info",
            labelCheckedClassName="active",
            options=[
                {'label': y_value, 'value': y_value} for y_value in y_axis_options
            ],
            value='Revenue'
            #style={'width': '25%','justify-content': 'center'}
            #labelStyle={"color": "black"},
            #inline=True
            #inputStyle={"background-color": "blue"}
        ),
     ],width={'size': 8, 'offset': 0, 'order': 2}, className="hstack gap-2" "radiobutton-group"),
    ],className='p-2 align-items-center'),

    dcc.Graph(id='revenue-graph'),
])



# Define callback to update graph
@app.callback(
    Output('revenue-graph', 'figure'),
    [Input('payment-category-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('equipment-id-dropdown', 'value'),
     Input('station-id-dropdown', 'value'),
     Input('transaction-type-dropdown', 'value'),
     Input('x-axis-radio', 'value'),
     Input('y-axis-radio', 'value')]  # Use radio items for y-axis selection
)
def update_graph(payment_mode, start_date, end_date, equipment_id, selected_station, transaction_type, x_axis_value, y_axis_value):
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

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
