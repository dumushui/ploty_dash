# -*- coding: utf-8 -*-
import dash
import os
import flask
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Video(src='/data/f.mp4')

server = app.server

@server.route('/data/<path:path>')
def serve_static(path):
    root_dir = os.getcwd()
    return flask.send_from_directory(os.path.join(root_dir, 'data'), path)

if __name__ == '__main__':
    app.run_server(debug=True)