import dash
import os
import flask
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from path_testing import files_
import dash_player as player

f = files_('data')

external_stylesheets = ['https:/codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.Img(id="logo-mobile", src="http://www.walterhuang.xyz/aidriving/logo.jpg"),
        dcc.RadioItems(
            options=[
            {'label': '良好', 'value': 'GOOD'},
            {'label': '复杂', 'value': 'BAD'},],
            value='GOOD',
            labelStyle={'display': 'inline-block'}
            ),
        dcc.RadioItems(
            options=[
            {'label': '良好', 'value': 'GOOD'},
            {'label': '复杂', 'value': 'BAD'},],
            value='GOOD',
            labelStyle={'display': 'inline-block'}
        ),









        html.Div(
                    className="video-outer-container",
                    children=html.Div(
                        className="video-container",
                        children=player.DashPlayer(
                            id="video-display",
                            url=f.return_relative_dir().__str__(),
                            loop=True,
                            playing=True,
                            controls=True,
                            volume=1,
                            width="100%",
                            height="100%",
                        ),
                    ),
                ),
        html.Button(id='submit-button', n_clicks=0, children='Submit'),
        html.Div(id='output-state')

], style={'columnCount': 2})







@app.callback(Output('video-display', 'url'),
              [Input('submit-button', 'n_clicks')])
def update_output(n_clicks):
    _ = f.pop_update()
    return f.return_relative_dir().__str__()


server = app.server

@server.route('/data/<path:path>')
def serve_static(path):
    root_dir = os.getcwd()
    return flask.send_from_directory(os.path.join(root_dir, 'data'), path)

if __name__ == '__main__':
    app.run_server(debug=True)