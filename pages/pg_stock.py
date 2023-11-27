import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd

from data import dfst
# import plotly.express as px

dash.register_page(__name__, path='/stock', name="Stock Insights")

for key in dfst.keys():
    dfst[key].columns = ["Category","Count","Station Id"]

layout = html.Div([
    # html.H4('Analysis of the restaurant sales'),
    html.Link(rel='stylesheet', href='/assets/ots_styles.css'),
   dbc.Col([
    html.P("Station ID:",style={'width': '30%','justify-content': 'center','marginLeft':'900px','font-family':'Roboto'}),
    dcc.Dropdown(id='stations',
        options=[{'label':station, 'value': station} for station in dfst['stock']['Station Id'].unique()],
        value='0303', clearable=True,
        style={'width': '50%','font-family':'Roboto'}
    ),
     ],width={'size': 10}, className="hstack gap-1"),
    # ],className='p-2 align-items-center date-range hstack gap-2'),
     dcc.Graph(id="graph",
              config={
        "displaylogo": False,
        'modeBarButtonsToRemove': ['pan2d','lasso2d']
    })
])


@callback(
    Output("graph", "figure"), 
    Input("stations", "value"))
def generate_chart(stations):

    fig = make_subplots(rows=1,cols=2,specs=[[{'type':'domain'},{'type':'domain'}]])

    labels = dfst['stock'][dfst['stock']['Category'] != 'No_of_Cards_Sold']['Category']
    values = dfst['stock']['Count']
    filtered_labels = dfst['stock'][dfst['stock']['Category'] == 'No_of_Cards_Sold']['Station Id']
    filtered_values = dfst['stock'][(dfst['stock']['Station Id'] == stations) & (dfst['stock']['Station Id'] != ' ')]['Count']
    fig.add_trace(go.Pie(labels=labels, values=values,name="Total Stock"),1,1)
    fig.add_trace(go.Pie(labels=filtered_labels,values=filtered_values,name="Cards Sold"),1,2)
    fig.update_traces(textposition='outside', textinfo='percent+label',hole=.6, hoverinfo="label+percent+name")

    fig.update_layout(
    # title_text="Stock",
    # Add annotations in the center of the donut pies.
    annotations=[dict(text='Total Stock', x=0.18, y=0.5, font_size=20, showarrow=False),
                 dict(text='Cards Sold', x=0.82, y=0.5, font_size=20, showarrow=False)])
    
    return fig