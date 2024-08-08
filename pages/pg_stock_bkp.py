# import dash
# from dash import html, dcc, callback
# from dash.dependencies import Input, Output
# import dash_bootstrap_components as dbc
# import plotly.graph_objs as go
# from plotly.subplots import make_subplots
# import pandas as pd
# import plotly.colors as plc
# import random
# import numpy as np

# from data import dfst

# dash.register_page(__name__, path='/stock', name="Stock Insights")

# for key in dfst.keys():
#     dfst[key].columns = ["Category", "Count", "Station Id", "Product Id"]

# stationid_filter = [stationid for stationid in dfst['stock']['Station Id'].unique() if stationid.strip() != '']

# layout = html.Div([
#     html.Link(rel='stylesheet', href='/assets/ots_styles.css'),
#     dbc.Col([
#         html.P("Station ID:", style={'width': '30%', 'justify-content': 'center', 'marginLeft': '900px',
#                                       'font-family': 'Roboto'}),
#         dcc.Dropdown(id='stations',
#                      options=[{'label': 'All', 'value': 'All'}] + [
#                          {'label': station, 'value': station} for station in stationid_filter],
#                      value='All', clearable=True,
#                      style={'width': '50%', 'font-family': 'Roboto'}
#                      ),
#     ], width={'size': 10}, className="hstack gap-1"),

#     dcc.Graph(id="graph",
#               config={
#                   "displaylogo": False,
#                   'modeBarButtonsToRemove': ['pan2d', 'lasso2d']
#               })
# ])


# @callback(
#     Output("graph", "figure"),
#     Input("stations", "value"))
# def generate_chart(stations):
#     fig = make_subplots(rows=1, cols=2, subplot_titles=["Total Stock", "Cards Sold and Product ID"],
#                         specs=[[{'type': 'pie'}, {'type': 'bar'}]])

#     labels = dfst['stock'][dfst['stock']['Category'] != 'No_of_Cards_Sold']['Category']
#     values = dfst['stock']['Count']
#     station_labels = dfst['stock'][dfst['stock']['Category'] == 'No_of_Cards_Sold']['Station Id']

#     if stations == 'All':
#         filtered_values = dfst['stock'][(dfst['stock']['Category'] == 'No_of_Cards_Sold')]['Count']
#     if stations != 'All':
#         filtered_values = dfst['stock'][(dfst['stock']['Category'] == 'No_of_Cards_Sold') & (
#                     dfst['stock']['Station Id'] == stations)]['Count']

#     product_master = ["Rupay Prepaid Card", "Visa", "Master"]

#     # Generate random colors for each bar
#     random_colors = random.sample(plc.qualitative.Set1, len(product_master))

#     pie_trace = go.Pie(labels=labels, values=values, name="Total Stock", legendgroup='group')  # , pull=[0, 0, 0, 0.2])
#     bar_Card_sold = go.Bar(x=station_labels, y=filtered_values, name="Cards Sold", marker_color='rgb(60, 133, 120)',
#                            showlegend=False)
#     bar_product_id = go.Bar(x=station_labels, y=dfst['stock'][
#         (dfst['stock']['Category'] != 'No_of_Cards_Sold') & (dfst['stock']['Station Id'] == stations)]['Count'],
#                            name="Product ID", marker_color=random_colors[0], showlegend=False)

#     # pie_trace.legend(loc='upper right')

#     fig.add_trace(pie_trace, row=1, col=1)
#     fig.add_trace(bar_Card_sold, row=1, col=2),
#     fig.add_trace(bar_product_id, row=1, col=2)

#     # Apply update_traces only to the Pie chart
#     fig.update_traces(textposition='inside', textinfo='label+percent+value', hole=0.6,
#                       hoverinfo="label+percent+value", selector=dict(type='pie'))
#     fig.update_traces(textposition='auto', selector=dict(type='bar'))

#     fig.update_layout(
#         xaxis_title="Station ID",
#         yaxis_title="Cards Sold",
#         annotations=[dict(text='Total Stock', x=0.15, y=0.47, font_size=20, showarrow=False)],
#         legend=dict(x=0.1, y=-0.1),
#         bargap=0.2,
#         barmode='stack',
#         bargroupgap=0.1,
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         font=dict(
#             family="Roboto",
#             size=14,
#             color="black"
#         ),
#         margin=dict(l=50, r=100, b=10, t=0),
#         height=600)

#     return fig
