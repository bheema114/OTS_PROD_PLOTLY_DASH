import dash
from dash import Dash,dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go

#external_css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css", ]

app = Dash(__name__,pages_folder='pages',use_pages=True)
server = app.server

pages = [
#{'name': 'Home', 'relative_path': '/', 'icon_url': '/assets/images/'},
{'name': 'Revenue', 'relative_path': '/revenue', 'icon_url': '/assets/images/revenue_icon.png'},
{'name': 'Ridership', 'relative_path': '/ridership', 'icon_url': '/assets/images/revenue_icon.png'},
{'name': 'Stock', 'relative_path': '/stock', 'icon_url': '/assets/images/revenue_icon.png'}
]

pages2 = [{'name': 'Hourly Ridership', 'relative_path': '/hourly', 'icon_url': '/assets/images/revenue_icon.png'}
]

app.layout = html.Div([

dbc.Row([

dbc.Col([
    html.Div([
        html.A(
            html.Div([
                html.Img(src=page['icon_url'], style={'width': '36px', 'height': '36px', 'margin-right': '16px'}),
                page['name']
            ]),
            href=page['relative_path'],
            className="button button_label"
        )
        for page in pages
    ], style={'display': 'flex'})

],width=4),

dbc.Col([

    html.Div([
            html.A(
                html.Div([
                    html.Img(src=page['icon_url'], style={'width': '36px', 'height': '36px', 'margin-right': '16px'}),
                    page['name']
                ]),
                href=page['relative_path'],
                className="button2 button_label2"
            )
            for page in pages2
        ]),

]),
],className='hstack'),
    dash.page_container
])

#  



# Add cache-control headers to prevent caching
@app.server.after_request
def add_no_cache_header(response):
    response.headers['Cache-Control'] = 'no-store, must-revalidate'
    return response

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
