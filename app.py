import plotly.graph_objs as go
import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table, State
import dash_bootstrap_components as dbc

from mysql_utils import sql_insert, sql_delete, sql_select
from mongodb_utils import get_faculty_info, get_universities, get_faculty
from neo4j_utils import get_scores

external_stylesheets = ['styles.css']

# Sample data for the charts
x = [1, 2, 3]
y1 = [4, 5, 6]
y2 = [7, 8, 9]
y3 = [10, 11, 12]
y4 = [13, 14, 15]
y5 = [16, 17, 18]

# Define the charts

# Figure 1
#--------------------------------
input1 = dcc.Input(id='input1', placeholder="Add a keyword")
submit1 = html.Button('add', id="submit1", n_clicks=0,)
input2 = dcc.Input(id='input2', placeholder="Delete a keyword")
delete1 = html.Button('delete', id='delete1', n_clicks=0)

table1 = dash_table.DataTable(
    columns=[{"name": "keyword", "id": "keyword"}],
    id="keyword_table",
    style_table={'overflowX': 'auto'}
)

table2 = dash_table.DataTable(
    columns=[{"name": "faculty_name", "id": "faculty_name"}, 
             {"name": "num_matches", "id": "num_matches"}, 
             {"name": "total_score", "id": "total_score"}],
    id="rec_prof_table",
    style_table={'overflowX': 'auto'}
)

table3 = dash_table.DataTable(
    columns=[{"name": "title", "id": "title"}, 
             {"name": "num_matches", "id": "num_matches"}, 
             {"name": "total_score", "id": "total_score"}],
    id="rec_pub_table",
    style_table={'overflowX': 'auto'}
)

@callback(
    Output("keyword_table", "data", allow_duplicate=True),
    Output("rec_prof_table", "data", allow_duplicate=True),
    Output("rec_pub_table", "data", allow_duplicate=True),
    State("input1", "value"),
    Input("submit1", "n_clicks"),
    prevent_initial_call=True
)
def add_keyword(input_value, n_clicks):
    if not input_value:
        return dash.no_update
    sql_insert(input_value)
    result1, result2, result3 = sql_select()
    return result1, result2, result3

@callback(
    Output("keyword_table", "data"),
    Output("rec_prof_table", "data"),
    Output("rec_pub_table", "data"),
    State("input2", "value"),
    Input("delete1", "n_clicks"),
)
def delete_keyword(input_value, n_clicks):
    if not input_value:
        return dash.no_update
    sql_delete(input_value)
    result1, result2, result3 = sql_select()
    return result1, result2, result3

# Figure 2
#--------------------------------
dropdown1 = dcc.Dropdown(get_universities(), placeholder="Select a University", id="dropdown1")
dropdown2 = dcc.Dropdown([], placeholder="Select a Faculty Member", id="dropdown2")

image1 = html.Img(id="prof_img", src="assets/No_Image_Available.jpg", alt="No Image Available")

row1 = html.Tr([html.Td("Name:"), html.Td(id="row1")])
row2 = html.Tr([html.Td("Position:"), html.Td(id="row2")])
row3 = html.Tr([html.Td("Email:"), html.Td(id="row3")])
row4 = html.Tr([html.Td("Phone:"), html.Td(id="row4")])
row5 = html.Tr([html.Td("Research:"), html.Td(id="row5")])
row6 = html.Tr([html.Td("Publications"), html.Td(id="row6")])
row7 = html.Tr([html.Td("University:"), html.Td(id="row7")])
table_body1 = [html.Tbody([row1, row2, row3, row4, row5, row6, row7])]
table4 = dbc.Table(table_body1)

@callback(
    Output("dropdown2", "options"),
    Input("dropdown1", "value")
)
def get_faculty_members(input_value):
    if not input_value:
        return dash.no_update
    return get_faculty(input_value)

@callback(
    Output("row1", "children"),
    Output("row2", "children"),
    Output("row3", "children"),
    Output("row4", "children"),
    Output("row5", "children"),
    Output("row6", "children"),
    Output("row7", "children"),
    Output("prof_img", "src"),
    Input("dropdown2", "value")
)
def get_info(input_value):
    if not input_value:
        return dash.no_update
    result = get_faculty_info(input_value)
    return result["name"], result["position"], result["email"], result["phone"], result["researchInterest"], result["publications"], result["affiliation"]["name"], result["photoUrl"]

# Figure 3
#--------------------------------
input3 = dcc.Input( id='input3', placeholder="Add a keyword")
submit2 = html.Button('submit', id="submit2", n_clicks=0)
graph1_layout = {
    # 'title': 'Top Universities By Keyword',
    'xaxis': {'title': 'University'},
    'yaxis': {'title': 'Keyword Score'},
}
graph1 = dcc.Graph(
    id="graph1",
    figure={
        'data': [],
        'layout': graph1_layout
    }
)

@callback(
    Output("graph1", "figure"),
    State("input3", "value"),
    Input("submit2", "n_clicks"),
)
def add_keyword_neo(input_value, n_clicks):
    if not input_value:
        return dash.no_update
    result = get_scores(input_value)
    x = list(result.keys())
    y = list(result.values())
    return {
        'data': [{'x': x, 'y': y, 'type': 'bar'}],
        'layout': graph1_layout
    }

# Figure 4
#--------------------------------
chart4 = dcc.Graph(
    id='chart4',
    figure={
        'data': [go.Scatter(x=x, y=y4, mode='lines')],
        'layout': go.Layout(title='Chart 4')
    }
)

# Figure 5
#--------------------------------
chart5 = dcc.Graph(
    id='chart5',
    figure={
        'data': [go.Scatter(x=x, y=y5, mode='lines')],
        'layout': go.Layout(title='Chart 5')
    }
)

# Figure 6
#--------------------------------
chart6 = dcc.Graph(
    id='chart6',
    figure={
        'data': [go.Scatter(x=x, y=y1, mode='lines')],
        'layout': go.Layout(title='Chart 6')
    }
)

# Define the layout
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                input1, submit1, input2, delete1
            ], className="figurecomponents"),
            html.H2("Favorite Keywords", style={"text-align":"center"}),
            html.Div([
                table1
            ], className="figurecomponents"),
            html.H2("Recommended Professors", style={"text-align":"center"}),
            html.Div([
                table2
            ], className="figurecomponents"),
            html.H2("Recommended Publications", style={"text-align":"center"}),
            html.Div([
                table3
            ], className="figurecomponents"),
        ], className="figure"),
        html.Div([
            html.H1("Faculty Directory", style={"text-align":"center"}),
            html.Div([
                dropdown1, dropdown2
            ], className="figurecomponents"),
            html.Div([
                image1, table4,
            ], className="figurecomponents")
        ], className="figure"),
        html.Div([
            html.H1("Top Universities By Keyword", style={"text-align":"center"}),
            html.Div([
                input3, submit2
            ], className="figurecomponents"),
            html.Div([
                graph1
            ], className="figurecomponents")
        ], className="figure")
    ], className="row"),
    html.Div([
        html.Div([
            html.Div([
                chart4
            ], className="figurecomponents"),
        ], className="figure"),
        html.Div([
            html.Div([
                chart5
            ], className="figurecomponents"),
        ], className="figure"),
        html.Div([
            html.Div([
                chart6
            ], className="figurecomponents"),
        ], className="figure")
    ], className="row")
])

if __name__ == '__main__':
    app.run_server(debug=True)