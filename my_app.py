import dash
import os
import flask
from textwrap import dedent
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from path_testing import files_
import dash_player as player

f = files_('data')

external_stylesheets = ['https:/codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)






def markdown_popup():
    return html.Div(
        id="markdown",
        className="modal",
        style={"display": "none"},
        children=(
            html.Div(
                className="markdown-container",
                children=[
                    html.Div(
                        className="close-container",
                        children=html.Button(
                            "Close",
                            id="markdown_close",
                            n_clicks=0,
                            className="closeButton",
                        ),
                    ),
                    html.Div(
                        className="markdown-text",
                        children=[
                            dcc.Markdown(
                                children=dedent(
                                    """
                                ##### What am I looking at?
                                
                                This app enhances visualization of objects detected using state-of-the-art Mobile Vision Neural Networks.
                                Most user generated videos are dynamic and fast-paced, which might be hard to interpret. A confidence
                                heatmap stays consistent through the video and intuitively displays the model predictions. The pie chart
                                lets you interpret how the object classes are divided, which is useful when analyzing videos with numerous
                                and differing objects.
                                ##### More about this Dash app
                                
                                The purpose of this demo is to explore alternative visualization methods for object detection. Therefore,
                                the visualizations, predictions and videos are not generated in real time, but done beforehand. To read
                                more about it, please visit the [project repo](https://github.com/plotly/dash-sample-apps/tree/master/apps/dash-object-detection).
                                """
                                )
                            )
                        ],
                    ),
                ],
            )
        ),
    )





app.layout = html.Div(
    children=[
        html.Img(id="logo-mobile", src="http://www.walterhuang.xyz/aidriving/logo.jpg"),
        html.Button("Learn More", id="learn-more-button", n_clicks=0),
        markdown_popup(),
   #      dcc.Markdown('''
			# #### Dash and Markdown

			# Dash supports [Markdown](http://commonmark.org/help).

			# Markdown is a simple way to write and format text.
			# It includes a syntax for things like **bold text** and *italics*,
			# [links](http://commonmark.org/help), inline `code` snippets, lists,
			# quotes, and more.
			# '''),
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
                            width="80%",
                            height="80%",
                        ),
                    ),
                ),
        html.Button(id='submit-button', n_clicks=0, children='Submit'),
        html.Div(id='output-state')

], style={'columnCount': 2})




# @app.callback(Output('output-help', 'children'),
#               [Input('help-button', 'n_clicks')])
# def help_(n_clicks):
#     return html.Div(
#     	style={"display": "none"},
#     	children=(
#     	dcc.Markdown(
#     		children=dedent('''
# 			### Dash and Markdown ###

# 			# Dash supports [Markdown](http://commonmark.org/help).

# 			# Markdown is a simple way to write and format text.
# 			# It includes a syntax for things like **bold text** and *italics*,
# 			# [links](http://commonmark.org/help), inline `code` snippets, lists,
# 			# quotes, and more.
# 			# ''')
# 			)
#     	)
#     	)
    





@app.callback(
    Output("markdown", "style"),
    [Input("learn-more-button", "n_clicks"), Input("markdown_close", "n_clicks")],
)
def update_click_output(button_click, close_click):
    ctx = dash.callback_context
    prop_id = ""
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if prop_id == "learn-more-button":
        return {"display": "block"}
    else:
        return {"display": "none"}











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