import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
# from plotly.graph_objs import Layout

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ], meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=0.4"}])
server = app.server

content_style = {
    'backgroundColor':'fae5df',

}

nav_style = {
    'backgroundColor':'#241a47',
    'fontFamily':'Times New Roman',
    'color':'white',
    'textAlign':'right'
}

content = html.Div(id='page-content', children=[], style=content_style)

nav = html.Div(dbc.Nav([
    dbc.NavItem(dbc.NavLink('Lumpsum Calculator', href='/lumpsum', active='exact', style={'color':'white'})),
    dbc.NavItem(dbc.NavLink('SIP Calculator', href='/sip', active='exact', style={'color':'white'})),
], style=nav_style))

lumpsum_page = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1('Mutual Funds Returns Calculator', style={'textAlign':'center'}),
            ])
        ]),
        dbc.Row([
            dbc.Col([

            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Label('Lumpsum Amount')
            ]),
            dbc.Col([
                dbc.Card(id='l-amount-display')
            ], style={'textAlign':'center'}, width=1)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Slider(min=0, max=100000, step=1000, id='l-amount-slider', value=5000)
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Label('Time Period')
            ]),
            dbc.Col([
                dbc.Card(id='l-time-display')
            ], style={'textAlign':'center'}, width=1)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Slider(min=0, max=30, step=1, id='l-time-slider', value=10)
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Label('Rate')
            ]),
            dbc.Col([
                dbc.Card(id='l-rate-display')
            ], style={'textAlign':'center'}, width=1)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Slider(min=0, max=30, step=1, id='l-rate-slider', value=10)
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Div(id='my-stats', children=[])
            ])
        ])
    ])
])

app.layout = html.Div([
    dcc.Location(id='url'),
    nav,
    content
])


@app.callback(
    Output('my-stats', 'children'),
    [Input('l-amount-slider', 'value'),
     Input('l-time-slider', 'value'),
     Input('l-rate-slider', 'value')]
)
def update_l_stats(amount, time, rate):
    total_inv = amount
    estimated = round(amount*(1+rate/100)**time - amount)
    total_value = total_inv + estimated
    labels = ['Total Investment', 'Estimated Returns']
    values = [total_inv, estimated]

    layout = go.Layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5)], layout=layout)
    fig.update_traces(marker=dict(colors=['#d93277', '#5dd9be']))

    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Amount Invested', style={'backgroundColor':'#241a47', 'color':'white'}),
                    dbc.CardBody(f'Rs. {amount}')
                ], style={'textAlign':'center'})
            ]),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Time Period', style={'backgroundColor':'#241a47', 'color':'white'}),
                    dbc.CardBody(f'{time} Years')
                ], style={'textAlign':'center'})
            ]),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Expected Rate of Return', style={'backgroundColor':'#241a47', 'color':'white'}),
                    dbc.CardBody(f'{rate}%')
                ], style={'textAlign':'center'})
            ])
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Total Investment', style={'backgroundColor':'#241a47', 'color':'white'}),
                    dbc.CardBody(f'Rs. {str(total_inv)}')
                ], style={'textAlign':'center'}),
                html.Br(),
                dbc.Card([
                    dbc.CardHeader('Estimated Returns', style={'backgroundColor':'#241a47', 'color':'white'}),
                    dbc.CardBody(f'Rs.{round(estimated)}')
                ], style={'textAlign':'center'}),
                html.Br(),
                dbc.Card([
                    dbc.CardHeader('Total Value', style={'backgroundColor':'#241a47', 'color':'white'}),
                    dbc.CardBody(f'Rs. {round(total_value)}')
                ], style={'textAlign':'center'})
            ]),
            dbc.Col([
                dbc.Card([
                    dcc.Graph(figure=fig)
                ])
            ])
        ])
    ])


@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def update_page(pathname):
    if pathname == '/lumpsum':
        return lumpsum_page






@app.callback(
    Output('l-amount-display', 'children'),
    Input('l-amount-slider', 'value')
)
def update_l_amount_card(value):
    return f'Rs. {value}'

@app.callback(
    Output('l-time-display', 'children'),
    Input('l-time-slider', 'value')
)
def update_l_time_card(value):
    return f'{value} Years'

@app.callback(
    Output('l-rate-display', 'children'),
    Input('l-rate-slider', 'value')
)
def update_l_time_card(value):
    return f'{value}%'

if __name__ == '__main__':
    app.run_server()