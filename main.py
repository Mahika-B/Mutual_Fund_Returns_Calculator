import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go


app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}])
server = app.server

content_style = {
    'backgroundColor':'fae5df',
    'padding':'2rem 1rem'
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
                html.H1('Mutual Funds Returns Calculator', style={'textAlign':'center', 'fontSize':18, 'fontFamily':'Times New Roman'}),
            ])
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.Label('Lumpsum Amount', style={'fontSize':12, 'fontFamily':'Times New Roman'})
            ]),
            dbc.Col([
                dbc.Card(id='l-amount-display', style={'backgroundColor':'#241a47', 'color':'white', 'fontFamily':'Times New Roman'})
            ], style={'textAlign':'center', 'fontSize':12}, width=3)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Slider(min=0, max=100000, step=1000, id='l-amount-slider', value=5000)
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Label('Time Period', style={'fontSize':12, 'fontFamily':'Times New Roman'})
            ]),
            dbc.Col([
                dbc.Card(id='l-time-display', style={'backgroundColor':'#241a47', 'color':'white', 'fontFamily':'Times New Roman'})
            ], style={'textAlign':'center', 'fontSize':12}, width=3)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Slider(min=0, max=30, step=1, id='l-time-slider', value=10)
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Label('Rate', style={'fontSize':12, 'fontFamily':'Times New Roman'})
            ]),
            dbc.Col([
                dbc.Card(id='l-rate-display', style={'backgroundColor':'#241a47', 'color':'white', 'fontFamily':'Times New Roman'})
            ], style={'textAlign':'center', 'fontSize':12}, width=3)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Slider(min=0, max=30, step=1, id='l-rate-slider', value=10)
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Div(id='l-my-stats', children=[])
            ])
        ])
    ])
])
sip_page = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1('SIP Returns Calculator', style={'textAlign':'center', 'fontSize':18, 'fontFamily':'Times New Roman'}),
            ])
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.Label('Monthly Investment', style={'fontSize':12, 'fontFamily':'Times New Roman'})
            ]),
            dbc.Col([
                dbc.Card(id='s-amount-display', style={'backgroundColor':'#241a47', 'color':'white', 'fontFamily':'Times New Roman'})
            ], style={'textAlign':'center', 'fontSize':12}, width=3)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Slider(min=0, max=100000, step=1000, id='s-amount-slider', value=5000)
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Label('Time Period', style={'fontSize':12, 'fontFamily':'Times New Roman'})
            ]),
            dbc.Col([
                dbc.Card(id='s-time-display', style={'backgroundColor':'#241a47', 'color':'white', 'fontFamily':'Times New Roman'})
            ], style={'textAlign':'center', 'fontSize':12}, width=3)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Slider(min=0, max=30, step=1, id='s-time-slider', value=10)
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Label('Rate', style={'fontSize':12, 'fontFamily':'Times New Roman'})
            ]),
            dbc.Col([
                dbc.Card(id='s-rate-display', style={'backgroundColor':'#241a47', 'color':'white', 'fontFamily':'Times New Roman'})
            ], style={'textAlign':'center', 'fontSize':12}, width=3)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Slider(min=0, max=30, step=1, id='s-rate-slider', value=10)
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Div(id='s-my-stats', children=[])
            ])
        ])
    ])
])
home_page = html.Div([
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.H1('Welcome to the Returns Calculator!'),
    html.Br(),
    html.H4('Calculate investment returns on the click of a button!'),
    html.Br(),
    html.Br(),
    html.H6('Choose calculator to begin.'),
    html.Br(),
], style={'backgroundColor': '#CE8CA5','color':'#F5E8DA' ,'textAlign':'center', 'fontFamily':'Times New Roman','height':550, 'padding':'0rem 1rem'})

app.layout = html.Div([
    dcc.Location(id='url'),
    nav,
    content
])




@app.callback(
    Output('l-my-stats', 'children'),
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

    layout = go.Layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin={'t':0, 'l':0,'b':0, 'r':0})
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5)], layout=layout)
    fig.update_traces(marker=dict(colors=['#d93277', '#5dd9be']))
    fig.update_layout(legend=dict(yanchor='bottom', y=0.01, orientation='h'))

    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Total Investment', style={'backgroundColor':'#241a47', 'color':'white', 'fontSize':10, 'fontFamily':'Times New Roman'}),
                    dbc.CardBody(f'Rs. {str(total_inv)}', style={'fontSize':12, 'fontFamily':'Times New Roman'})
                ], style={'textAlign':'center'}),
            ]),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Estimated Returns', style={'backgroundColor':'#241a47', 'color':'white', 'fontSize':10}),
                    dbc.CardBody(f'Rs.{round(estimated)}', style={'fontSize':12})
                ], style={'textAlign':'center', 'fontFamily':'Times New Roman'}),
            ]),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Value of Investment', style={'backgroundColor':'#241a47', 'color':'white', 'fontSize':10}),
                    dbc.CardBody(f'Rs. {round(total_value)}', style={'fontSize':12})
                ], style={'textAlign':'center', 'fontFamily':'Times New Roman'})
            ]),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dcc.Graph(figure=fig)
                ])
            ])
        ])
    ])



@app.callback(
    Output('s-my-stats', 'children'),
    [Input('s-amount-slider', 'value'),
     Input('s-time-slider', 'value'),
     Input('s-rate-slider', 'value')]
)
def update_s_stats(amount, time, rate):
    total_inv = amount*time*12
    estimated = amount*(((1+rate/1200)**(time*12) - 1)/(rate/1200))*(1+(rate/1200)) - total_inv
    total_value = total_inv + estimated
    labels = ['Total Investment', 'Estimated Returns']
    values = [total_inv, estimated]

    layout = go.Layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin={'t':0, 'b':0, 'l':0, 'r':0})
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5)], layout=layout)
    fig.update_traces(marker=dict(colors=['#d93277', '#5dd9be']))
    fig.update_layout(legend=dict(yanchor='bottom', y=0.01, orientation='h'))

    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Total Investment', style={'backgroundColor':'#241a47', 'color':'white', 'fontSize':10}),
                    dbc.CardBody(f'Rs. {str(total_inv)}', style={'fontSize':12})
                ], style={'textAlign':'center', 'fontFamily':'Times New Roman'}),
            ]),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Estimated Returns', style={'backgroundColor':'#241a47', 'color':'white', 'fontSize':10}),
                    dbc.CardBody(f'Rs.{round(estimated)}', style={'fontSize':12})
                ], style={'textAlign':'center', 'fontFamily':'Times New Roman'})
            ]),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Value of Investment', style={'backgroundColor':'#241a47', 'color':'white', 'fontSize':10}),
                    dbc.CardBody(f'Rs. {round(total_value)}', style={'fontSize':12})
                ], style={'textAlign':'center', 'fontFamily':'Times New Roman'})
            ]),
        ]),
        html.Br(),
        dbc.Row([
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
    if pathname == '/sip':
        return sip_page
    if pathname == '/':
        return home_page


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

@app.callback(
    Output('s-amount-display', 'children'),
    Input('s-amount-slider', 'value')
)
def update_s_amount_card(value):
    return f'Rs. {value}'

@app.callback(
    Output('s-time-display', 'children'),
    Input('s-time-slider', 'value')
)
def update_s_time_card(value):
    return f'{value} Years'

@app.callback(
    Output('s-rate-display', 'children'),
    Input('s-rate-slider', 'value')
)
def update_s_time_card(value):
    return f'{value}%'


if __name__ == '__main__':
    app.run_server()