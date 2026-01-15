from dash import Dash, dcc, html
# from src.components import graph_age
# from src.components import map_sites

def launch_dashboard():
    app = Dash(__name__)

    # fig = graph_age.multi_trace_age()

    app.layout = html.Div(children=[
        html.H1(children='Olympic Data Dashboard',
                style={'textAlign': 'center', 'color': '#7FDBFF'}),

        # dcc.Graph(
        #     id='age-graph',
        #     figure=fig
        # ),
        html.Iframe(
            srcDoc=open("html/fig_age.html", 'r').read(),
            style={"width": "100%", "height": "600px", "border": "none"}
        ),

        html.Iframe(
            srcDoc=open("html/map_sites.html", 'r').read(),
            style={"width": "100%", "height": "600px", "border": "none"}
        ),

    ])

    app.run(debug=True)

if __name__ == '__main__':
    launch_dashboard()