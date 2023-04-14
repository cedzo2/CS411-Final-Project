import plotly.graph_objs as go
from dash import Dash, html, dcc

# Sample data for the charts
x = [1, 2, 3]
y1 = [4, 5, 6]
y2 = [7, 8, 9]
y3 = [10, 11, 12]
y4 = [13, 14, 15]
y5 = [16, 17, 18]

# Define the charts
chart1 = dcc.Graph(
    id='chart1',
    figure={
        'data': [go.Scatter(x=x, y=y1, mode='lines')],
        'layout': go.Layout(title='Chart 1')
    },
    style={'width': '30%', 'display': 'inline-block'}
)

chart2 = dcc.Graph(
    id='chart2',
    figure={
        'data': [go.Scatter(x=x, y=y2, mode='lines')],
        'layout': go.Layout(title='Chart 2')
    },
    style={'width': '30%', 'display': 'inline-block'}
)

chart3 = dcc.Graph(
    id='chart3',
    figure={
        'data': [go.Scatter(x=x, y=y3, mode='lines')],
        'layout': go.Layout(title='Chart 3')
    },
    style={'width': '30%', 'display': 'inline-block'}
)

chart4 = dcc.Graph(
    id='chart4',
    figure={
        'data': [go.Scatter(x=x, y=y4, mode='lines')],
        'layout': go.Layout(title='Chart 4')
    },
    style={'width': '30%', 'display': 'inline-block'}
)

chart5 = dcc.Graph(
    id='chart5',
    figure={
        'data': [go.Scatter(x=x, y=y5, mode='lines')],
        'layout': go.Layout(title='Chart 5')
    },
    style={'width': '30%', 'display': 'inline-block'}
)

chart6 = dcc.Graph(
    id='chart6',
    figure={
        'data': [go.Scatter(x=x, y=y1, mode='lines')],
        'layout': go.Layout(title='Chart 6')
    },
    style={'width': '30%', 'display': 'inline-block'}
)

# Define the layout
app = Dash(__name__)
app.layout = html.Div([
    html.Div([
        html.H1('CS411 Final Project'),
    ], className="row", style={'textAlign': 'center'}),
    html.Div([
        chart1, chart2, chart3,
    ], className="row"),
    html.Div([
        chart4, chart5, chart6,
    ], className="row")
], style={'height': '70vh'})

if __name__ == '__main__':
    app.run_server(debug=True)